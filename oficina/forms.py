from django import forms
from django.forms import formset_factory

from .models import Cliente, Orcamento, Servico, Veiculo


class StyledModelForm(forms.ModelForm):
    """Aplica classes consistentes aos controles dos formulários."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")


class ClienteForm(StyledModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "telefone", "email", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Nome do cliente"}),
            "telefone": forms.TextInput(attrs={"autocomplete": "tel", "placeholder": "(00) 00000-0000"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "cliente@exemplo.com"}),
        }


class VeiculoForm(StyledModelForm):
    class Meta:
        model = Veiculo
        fields = ["cliente", "marca", "modelo", "ano", "placa"]
        widgets = {
            "marca": forms.TextInput(attrs={"placeholder": "Ex.: Fiat"}),
            "modelo": forms.TextInput(attrs={"placeholder": "Ex.: Uno"}),
            "ano": forms.NumberInput(attrs={"min": "1900", "max": "2100"}),
            "placa": forms.TextInput(attrs={"placeholder": "Opcional"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cliente"].queryset = Cliente.objects.filter(ativo=True).order_by("nome")


class ServicoForm(StyledModelForm):
    class Meta:
        model = Servico
        fields = ["nome", "descricao", "preco", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Revisão preventiva"}),
            "descricao": forms.TextInput(attrs={"placeholder": "Descrição resumida do serviço"}),
            "preco": forms.NumberInput(attrs={"min": "0.01", "step": "0.01", "placeholder": "0,00"}),
        }


class OrcamentoForm(StyledModelForm):
    class Meta:
        model = Orcamento
        fields = ["cliente", "veiculo", "status", "validade_dias", "observacoes"]
        widgets = {
            "validade_dias": forms.NumberInput(attrs={"min": "1", "max": "90"}),
            "observacoes": forms.Textarea(attrs={"rows": 3, "placeholder": "Informações adicionais (opcional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cliente"].queryset = Cliente.objects.filter(ativo=True).order_by("nome")
        self.fields["veiculo"].queryset = Veiculo.objects.select_related("cliente").order_by("cliente__nome", "marca", "modelo")
        self.fields["status"].initial = Orcamento.Status.ANALISE
        self.fields["validade_dias"].initial = 7

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get("cliente")
        veiculo = cleaned_data.get("veiculo")
        if cliente and veiculo and veiculo.cliente_id != cliente.pk:
            self.add_error("veiculo", "O veículo selecionado não pertence ao cliente informado.")
        return cleaned_data


class ItemOrcamentoForm(forms.Form):
    servico = forms.ModelChoiceField(
        queryset=Servico.objects.none(),
        label="Serviço",
        empty_label="Selecione um serviço",
    )
    quantidade = forms.IntegerField(label="Quantidade", min_value=1, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["servico"].queryset = Servico.objects.filter(ativo=True).order_by("nome")
        self.fields["servico"].label_from_instance = lambda obj: f"{obj.nome} — R$ {obj.preco:.2f}"
        self.fields["servico"].widget.attrs.update({"class": "form-select"})
        self.fields["quantidade"].widget.attrs.update({"class": "form-control", "min": "1"})


ItemOrcamentoFormSet = formset_factory(
    ItemOrcamentoForm,
    extra=1,
    min_num=1,
    validate_min=True,
    max_num=10,
    validate_max=True,
    can_delete=True,
)
