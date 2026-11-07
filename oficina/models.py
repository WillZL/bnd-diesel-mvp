from decimal import Decimal
from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Cliente(models.Model):
    nome = models.CharField("nome", max_length=120)
    telefone = models.CharField("telefone", max_length=25, blank=True)
    email = models.EmailField("e-mail", blank=True)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)
    ativo = models.BooleanField("ativo", default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self) -> str:
        return self.nome


class Veiculo(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="veiculos", verbose_name="cliente"
    )
    marca = models.CharField("marca", max_length=60)
    modelo = models.CharField("modelo", max_length=80)
    ano = models.PositiveSmallIntegerField(
        "ano", validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    placa = models.CharField("placa (opcional)", max_length=10, blank=True)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        ordering = ["marca", "modelo", "ano"]
        verbose_name = "veículo"
        verbose_name_plural = "veículos"

    def __str__(self) -> str:
        return f"{self.marca} {self.modelo} · {self.ano} — {self.cliente.nome}"


class Servico(models.Model):
    nome = models.CharField("nome do serviço", max_length=120)
    descricao = models.CharField("descrição", max_length=240, blank=True)
    preco = models.DecimalField(
        "preço", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    ativo = models.BooleanField("disponível para novos orçamentos", default=True)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "serviço"
        verbose_name_plural = "serviços"

    def __str__(self) -> str:
        return self.nome


class Orcamento(models.Model):
    class Status(models.TextChoices):
        ANALISE = "ANALISE", "Em análise"
        APROVADO = "APROVADO", "Aprovado"
        RECUSADO = "RECUSADO", "Recusado"

    codigo = models.CharField("código", max_length=20, unique=True, editable=False, blank=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="orcamentos", verbose_name="cliente"
    )
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.PROTECT, related_name="orcamentos", verbose_name="veículo"
    )
    status = models.CharField(
        "status", max_length=12, choices=Status.choices, default=Status.ANALISE
    )
    validade_dias = models.PositiveSmallIntegerField(
        "validade (dias)", default=7, validators=[MinValueValidator(1), MaxValueValidator(90)]
    )
    observacoes = models.TextField("observações", blank=True)
    criado_em = models.DateTimeField("criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-criado_em", "-pk"]
        verbose_name = "orçamento"
        verbose_name_plural = "orçamentos"

    def __str__(self) -> str:
        return self.codigo or f"Orçamento #{self.pk or 'novo'}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.codigo:
            # Usa um identificador temporário exclusivo para evitar colisões
            # de strings vazias em criações simultâneas.
            self.codigo = f"TMP-{uuid4().hex[:16]}"
        super().save(*args, **kwargs)
        if is_new and self.codigo.startswith("TMP-"):
            self.codigo = f"ORC-{self.pk:05d}"
            type(self).objects.filter(pk=self.pk).update(codigo=self.codigo)

    @property
    def subtotal(self) -> Decimal:
        return sum((item.subtotal for item in self.itens.all()), Decimal("0.00"))

    @property
    def total(self) -> Decimal:
        # O MVP não aplica descontos; total corresponde à soma dos itens.
        return self.subtotal

    @property
    def status_class(self) -> str:
        return {
            self.Status.ANALISE: "status-analysis",
            self.Status.APROVADO: "status-approved",
            self.Status.RECUSADO: "status-refused",
        }.get(self.status, "status-neutral")


class ItemOrcamento(models.Model):
    orcamento = models.ForeignKey(
        Orcamento, on_delete=models.CASCADE, related_name="itens", verbose_name="orçamento"
    )
    servico = models.ForeignKey(
        Servico, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="itens_orcamento", verbose_name="serviço de origem"
    )
    descricao = models.CharField("descrição do serviço", max_length=120)
    quantidade = models.PositiveSmallIntegerField(
        "quantidade", validators=[MinValueValidator(1)]
    )
    valor_unitario = models.DecimalField("valor unitário", max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["pk"]
        verbose_name = "item do orçamento"
        verbose_name_plural = "itens do orçamento"

    def __str__(self) -> str:
        return self.descricao

    @property
    def subtotal(self) -> Decimal:
        return self.quantidade * self.valor_unitario
