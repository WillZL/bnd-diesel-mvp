from decimal import Decimal

from django.core.management.base import BaseCommand

from oficina.models import Cliente, ItemOrcamento, Orcamento, Servico, Veiculo


class Command(BaseCommand):
    help = "Cria cadastros e um orçamento com dados exclusivamente demonstrativos."

    def handle(self, *args, **options):
        cliente, _ = Cliente.objects.get_or_create(
            nome="Cliente Demonstração",
            defaults={"telefone": "(11) 90000-0000", "email": "demo@example.com"},
        )
        veiculo, _ = Veiculo.objects.get_or_create(
            cliente=cliente,
            marca="Fiat",
            modelo="Uno",
            ano=2018,
            defaults={"placa": "DEMO000"},
        )
        servico, _ = Servico.objects.get_or_create(
            nome="Revisão preventiva",
            defaults={"descricao": "Inspeção geral do veículo", "preco": Decimal("250.00")},
        )
        orcamento = Orcamento.objects.filter(cliente=cliente, veiculo=veiculo).first()
        if orcamento is None:
            orcamento = Orcamento.objects.create(
                cliente=cliente, veiculo=veiculo, status=Orcamento.Status.ANALISE
            )
        if not orcamento.itens.exists():
            ItemOrcamento.objects.create(
                orcamento=orcamento,
                servico=servico,
                descricao=servico.nome,
                quantidade=1,
                valor_unitario=servico.preco,
            )
        self.stdout.write(self.style.SUCCESS(
            f"Dados demonstrativos disponíveis. Orçamento: {orcamento.codigo}."
        ))
