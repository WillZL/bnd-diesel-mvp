from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase, Client as DjangoClient
from django.urls import reverse

from .models import Cliente, ItemOrcamento, Orcamento, Servico, Veiculo


class OficinaFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin-teste", password="Senha-temporaria-2026"
        )
        self.client = DjangoClient()
        self.client.force_login(self.user)
        self.cliente = Cliente.objects.create(
            nome="Cliente Demonstração", telefone="(11) 90000-0000", email="demo@example.com"
        )
        self.veiculo = Veiculo.objects.create(
            cliente=self.cliente, marca="Fiat", modelo="Uno", ano=2018
        )
        self.servico = Servico.objects.create(
            nome="Revisão preventiva", descricao="Inspeção geral", preco=Decimal("250.00")
        )

    def test_dashboard_requires_authentication(self):
        visitante = DjangoClient()
        response = visitante.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_dashboard_loads_for_authenticated_user(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visão geral")

    def test_create_budget_persists_budget_and_item(self):
        payload = {
            "cliente": str(self.cliente.pk),
            "veiculo": str(self.veiculo.pk),
            "status": Orcamento.Status.ANALISE,
            "validade_dias": "7",
            "observacoes": "Registro de demonstração",
            "itens-TOTAL_FORMS": "1",
            "itens-INITIAL_FORMS": "0",
            "itens-MIN_NUM_FORMS": "1",
            "itens-MAX_NUM_FORMS": "10",
            "itens-0-servico": str(self.servico.pk),
            "itens-0-quantidade": "2",
        }
        response = self.client.post(reverse("orcamento-create"), payload)
        self.assertRedirects(response, reverse("orcamento-list"))
        orcamento = Orcamento.objects.get()
        item = ItemOrcamento.objects.get(orcamento=orcamento)
        self.assertEqual(orcamento.codigo, "ORC-00001")
        self.assertEqual(item.descricao, "Revisão preventiva")
        self.assertEqual(item.valor_unitario, Decimal("250.00"))
        self.assertEqual(orcamento.total, Decimal("500.00"))

    def test_budget_rejects_vehicle_from_another_client(self):
        outro_cliente = Cliente.objects.create(nome="Outro cliente")
        payload = {
            "cliente": str(outro_cliente.pk),
            "veiculo": str(self.veiculo.pk),
            "status": Orcamento.Status.ANALISE,
            "validade_dias": "7",
            "itens-TOTAL_FORMS": "1",
            "itens-INITIAL_FORMS": "0",
            "itens-MIN_NUM_FORMS": "1",
            "itens-MAX_NUM_FORMS": "10",
            "itens-0-servico": str(self.servico.pk),
            "itens-0-quantidade": "1",
        }
        response = self.client.post(reverse("orcamento-create"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Orcamento.objects.count(), 0)
        self.assertContains(response, "não pertence ao cliente")

    def test_client_can_be_created(self):
        response = self.client.post(reverse("cliente-create"), {
            "nome": "Novo Cliente",
            "telefone": "",
            "email": "",
            "ativo": "on",
        })
        self.assertRedirects(response, reverse("cliente-list"))
        self.assertTrue(Cliente.objects.filter(nome="Novo Cliente").exists())

    def test_budget_status_changes_only_through_post(self):
        orcamento = Orcamento.objects.create(cliente=self.cliente, veiculo=self.veiculo)
        get_response = self.client.get(reverse("orcamento-status", args=[orcamento.pk]))
        self.assertEqual(get_response.status_code, 405)
        post_response = self.client.post(
            reverse("orcamento-status", args=[orcamento.pk]),
            {"status": Orcamento.Status.APROVADO},
        )
        self.assertRedirects(post_response, reverse("orcamento-list"))
        orcamento.refresh_from_db()
        self.assertEqual(orcamento.status, Orcamento.Status.APROVADO)

    def test_budget_list_can_search_by_code(self):
        orcamento = Orcamento.objects.create(cliente=self.cliente, veiculo=self.veiculo)
        response = self.client.get(reverse("orcamento-list"), {"q": orcamento.codigo})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, orcamento.codigo)

    def test_service_price_is_copied_to_budget_item(self):
        orcamento = Orcamento.objects.create(cliente=self.cliente, veiculo=self.veiculo)
        ItemOrcamento.objects.create(
            orcamento=orcamento,
            servico=self.servico,
            descricao=self.servico.nome,
            quantidade=1,
            valor_unitario=self.servico.preco,
        )
        self.servico.preco = Decimal("300.00")
        self.servico.save()
        item = orcamento.itens.get()
        self.assertEqual(item.valor_unitario, Decimal("250.00"))
