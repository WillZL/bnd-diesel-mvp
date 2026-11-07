# Generated as the initial schema for the BND Diesel MVP.
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120, verbose_name="nome")),
                ("telefone", models.CharField(blank=True, max_length=25, verbose_name="telefone")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="e-mail")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="criado em")),
                ("ativo", models.BooleanField(default=True, verbose_name="ativo")),
            ],
            options={"verbose_name": "cliente", "verbose_name_plural": "clientes", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="Servico",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120, verbose_name="nome do serviço")),
                ("descricao", models.CharField(blank=True, max_length=240, verbose_name="descrição")),
                ("preco", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal("0.01"))], verbose_name="preço")),
                ("ativo", models.BooleanField(default=True, verbose_name="disponível para novos orçamentos")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="criado em")),
            ],
            options={"verbose_name": "serviço", "verbose_name_plural": "serviços", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="Veiculo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("marca", models.CharField(max_length=60, verbose_name="marca")),
                ("modelo", models.CharField(max_length=80, verbose_name="modelo")),
                ("ano", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)], verbose_name="ano")),
                ("placa", models.CharField(blank=True, max_length=10, verbose_name="placa (opcional)")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="criado em")),
                ("cliente", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="veiculos", to="oficina.cliente", verbose_name="cliente")),
            ],
            options={"verbose_name": "veículo", "verbose_name_plural": "veículos", "ordering": ["marca", "modelo", "ano"]},
        ),
        migrations.CreateModel(
            name="Orcamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(blank=True, editable=False, max_length=20, unique=True, verbose_name="código")),
                ("status", models.CharField(choices=[("ANALISE", "Em análise"), ("APROVADO", "Aprovado"), ("RECUSADO", "Recusado")], default="ANALISE", max_length=12, verbose_name="status")),
                ("validade_dias", models.PositiveSmallIntegerField(default=7, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(90)], verbose_name="validade (dias)")),
                ("observacoes", models.TextField(blank=True, verbose_name="observações")),
                ("criado_em", models.DateTimeField(auto_now_add=True, verbose_name="criado em")),
                ("atualizado_em", models.DateTimeField(auto_now=True, verbose_name="atualizado em")),
                ("cliente", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orcamentos", to="oficina.cliente", verbose_name="cliente")),
                ("veiculo", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orcamentos", to="oficina.veiculo", verbose_name="veículo")),
            ],
            options={"verbose_name": "orçamento", "verbose_name_plural": "orçamentos", "ordering": ["-criado_em", "-pk"]},
        ),
        migrations.CreateModel(
            name="ItemOrcamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("descricao", models.CharField(max_length=120, verbose_name="descrição do serviço")),
                ("quantidade", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name="quantidade")),
                ("valor_unitario", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="valor unitário")),
                ("orcamento", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="itens", to="oficina.orcamento", verbose_name="orçamento")),
                ("servico", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="itens_orcamento", to="oficina.servico", verbose_name="serviço de origem")),
            ],
            options={"verbose_name": "item do orçamento", "verbose_name_plural": "itens do orçamento", "ordering": ["pk"]},
        ),
    ]
