from django.contrib import admin

from .models import Cliente, ItemOrcamento, Orcamento, Servico, Veiculo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "email", "ativo")
    search_fields = ("nome", "telefone", "email")
    list_filter = ("ativo",)


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ("marca", "modelo", "ano", "cliente", "placa")
    search_fields = ("marca", "modelo", "placa", "cliente__nome")
    list_filter = ("ano", "marca")


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "ativo")
    search_fields = ("nome", "descricao")
    list_filter = ("ativo",)


class ItemOrcamentoInline(admin.TabularInline):
    model = ItemOrcamento
    extra = 0
    readonly_fields = ("descricao", "quantidade", "valor_unitario")


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "cliente", "veiculo", "status", "criado_em")
    search_fields = ("codigo", "cliente__nome", "veiculo__modelo")
    list_filter = ("status", "criado_em")
    inlines = (ItemOrcamentoInline,)
