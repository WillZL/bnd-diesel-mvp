from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.db.models import Q, Count
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import ClienteForm, ItemOrcamentoFormSet, OrcamentoForm, ServicoForm, VeiculoForm
from .models import Cliente, ItemOrcamento, Orcamento, Servico, Veiculo


@login_required
def dashboard(request):
    context = {
        "page_title": "Visão geral",
        "orcamentos_analise": Orcamento.objects.filter(status=Orcamento.Status.ANALISE).count(),
        "orcamentos_aprovados": Orcamento.objects.filter(status=Orcamento.Status.APROVADO).count(),
        "clientes_ativos": Cliente.objects.filter(ativo=True).count(),
        "recentes": Orcamento.objects.select_related("cliente", "veiculo").prefetch_related("itens")[:5],
    }
    return render(request, "core/dashboard.html", context)


class OficinaListView(LoginRequiredMixin, ListView):
    template_name = "core/object_list.html"
    context_object_name = "registros"
    paginate_by = 15
    model = None
    object_type = ""
    page_title = ""
    page_description = ""
    create_url = ""
    search_placeholder = "Buscar registros"
    search_fields = ()

    def get_queryset(self):
        queryset = self.model.objects.all()
        termo = self.request.GET.get("q", "").strip()
        if termo:
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": termo})
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "page_title": self.page_title,
            "page_description": self.page_description,
            "object_type": self.object_type,
            "create_url": self.create_url,
            "search_placeholder": self.search_placeholder,
            "termo": self.request.GET.get("q", ""),
        })
        return context


class ClienteListView(OficinaListView):
    model = Cliente
    object_type = "clientes"
    page_title = "Clientes"
    page_description = "Mantenha organizados os cadastros e os meios de contato dos clientes."
    create_url = "cliente-create"
    search_placeholder = "Buscar por nome, telefone ou e-mail"
    search_fields = ("nome", "telefone", "email")


class VeiculoListView(OficinaListView):
    model = Veiculo
    object_type = "veiculos"
    page_title = "Veículos"
    page_description = "Consulte os veículos e seus respectivos clientes."
    create_url = "veiculo-create"
    search_placeholder = "Buscar por cliente, marca, modelo ou placa"
    search_fields = ("cliente__nome", "marca", "modelo", "placa")

    def get_queryset(self):
        return super().get_queryset().select_related("cliente")


class ServicoListView(OficinaListView):
    model = Servico
    object_type = "servicos"
    page_title = "Serviços"
    page_description = "Cadastre os serviços e os valores utilizados na elaboração de orçamentos."
    create_url = "servico-create"
    search_placeholder = "Buscar por nome ou descrição"
    search_fields = ("nome", "descricao")


class BaseFormContext:
    page_title = "Cadastro"
    page_description = "Preencha as informações solicitadas."
    cancel_url = "dashboard"
    submit_label = "Salvar"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "page_title": self.page_title,
            "page_description": self.page_description,
            "cancel_url": self.cancel_url,
            "submit_label": self.submit_label,
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registro salvo com sucesso.")
        return response


class BaseCreateView(LoginRequiredMixin, BaseFormContext, CreateView):
    template_name = "core/form.html"


class BaseUpdateView(LoginRequiredMixin, BaseFormContext, UpdateView):
    template_name = "core/form.html"
    submit_label = "Salvar alterações"


class BaseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "core/confirm_delete.html"
    success_message = "Registro excluído com sucesso."
    cancel_url = "dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.cancel_url
        context["page_title"] = "Excluir registro"
        return context

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "Este registro possui informações vinculadas e não pode ser excluído. "
                "Desative-o ou revise os vínculos antes de tentar novamente.",
            )
            return redirect(self.get_success_url())
        messages.success(self.request, self.success_message)
        return response


class ClienteCreateView(BaseCreateView):
    model = Cliente
    form_class = ClienteForm
    page_title = "Novo cliente"
    page_description = "Registre apenas as informações necessárias para identificar e contatar o cliente."
    cancel_url = "cliente-list"
    success_url = reverse_lazy("cliente-list")


class ClienteUpdateView(BaseUpdateView):
    model = Cliente
    form_class = ClienteForm
    page_title = "Editar cliente"
    page_description = "Atualize os dados do cadastro selecionado."
    cancel_url = "cliente-list"
    success_url = reverse_lazy("cliente-list")


class ClienteDeleteView(BaseDeleteView):
    model = Cliente
    cancel_url = "cliente-list"
    success_url = reverse_lazy("cliente-list")
    success_message = "Cliente excluído com sucesso."


class VeiculoCreateView(BaseCreateView):
    model = Veiculo
    form_class = VeiculoForm
    page_title = "Novo veículo"
    page_description = "Associe o veículo a um cliente cadastrado."
    cancel_url = "veiculo-list"
    success_url = reverse_lazy("veiculo-list")


class VeiculoUpdateView(BaseUpdateView):
    model = Veiculo
    form_class = VeiculoForm
    page_title = "Editar veículo"
    page_description = "Atualize as informações do veículo."
    cancel_url = "veiculo-list"
    success_url = reverse_lazy("veiculo-list")


class VeiculoDeleteView(BaseDeleteView):
    model = Veiculo
    cancel_url = "veiculo-list"
    success_url = reverse_lazy("veiculo-list")
    success_message = "Veículo excluído com sucesso."


class ServicoCreateView(BaseCreateView):
    model = Servico
    form_class = ServicoForm
    page_title = "Novo serviço"
    page_description = "Cadastre uma descrição e um valor de referência para o serviço."
    cancel_url = "servico-list"
    success_url = reverse_lazy("servico-list")


class ServicoUpdateView(BaseUpdateView):
    model = Servico
    form_class = ServicoForm
    page_title = "Editar serviço"
    page_description = "Atualize as informações e a disponibilidade do serviço."
    cancel_url = "servico-list"
    success_url = reverse_lazy("servico-list")


class ServicoDeleteView(BaseDeleteView):
    model = Servico
    cancel_url = "servico-list"
    success_url = reverse_lazy("servico-list")
    success_message = "Serviço excluído com sucesso."


@login_required
def orcamento_list(request):
    queryset = (
        Orcamento.objects.select_related("cliente", "veiculo")
        .prefetch_related("itens")
        .order_by("-criado_em", "-pk")
    )
    termo = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    if termo:
        queryset = queryset.filter(
            Q(codigo__icontains=termo)
            | Q(cliente__nome__icontains=termo)
            | Q(veiculo__marca__icontains=termo)
            | Q(veiculo__modelo__icontains=termo)
        )
    valid_statuses = {value for value, _label in Orcamento.Status.choices}
    if status in valid_statuses:
        queryset = queryset.filter(status=status)
    else:
        status = ""
    return render(request, "core/orcamento_list.html", {
        "page_title": "Orçamentos",
        "orcamentos": queryset,
        "termo": termo,
        "status_atual": status,
        "status_choices": Orcamento.Status.choices,
    })


@login_required
def orcamento_create(request):
    if request.method == "POST":
        form = OrcamentoForm(request.POST)
        formset = ItemOrcamentoFormSet(request.POST, prefix="itens")
        form_is_valid = form.is_valid()
        formset_is_valid = formset.is_valid()
        if form_is_valid and formset_is_valid:
            with transaction.atomic():
                orcamento = form.save()
                for item_form in formset:
                    dados = item_form.cleaned_data
                    if not dados or dados.get("DELETE"):
                        continue
                    servico = dados["servico"]
                    ItemOrcamento.objects.create(
                        orcamento=orcamento,
                        servico=servico,
                        descricao=servico.nome,
                        quantidade=dados["quantidade"],
                        valor_unitario=servico.preco,
                    )
            messages.success(request, f"Orçamento {orcamento.codigo} criado com sucesso.")
            return redirect("orcamento-list")
    else:
        form = OrcamentoForm()
        formset = ItemOrcamentoFormSet(prefix="itens")
    return render(request, "core/orcamento_form.html", {
        "page_title": "Criar orçamento",
        "form": form,
        "formset": formset,
        "tem_clientes": Cliente.objects.filter(ativo=True).exists(),
        "tem_veiculos": Veiculo.objects.filter(cliente__ativo=True).exists(),
        "tem_servicos": Servico.objects.filter(ativo=True).exists(),
    })


@login_required
@require_POST
def orcamento_status(request, pk):
    orcamento = get_object_or_404(Orcamento, pk=pk)
    novo_status = request.POST.get("status", "")
    valid_statuses = {value for value, _label in Orcamento.Status.choices}
    if novo_status not in valid_statuses:
        messages.error(request, "Selecione uma situação válida para o orçamento.")
        return redirect("orcamento-list")
    orcamento.status = novo_status
    orcamento.save(update_fields=["status", "atualizado_em"])
    messages.success(request, f"Status de {orcamento.codigo} atualizado para {orcamento.get_status_display()}.")
    return redirect("orcamento-list")
