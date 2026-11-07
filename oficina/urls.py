from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("clientes/", views.ClienteListView.as_view(), name="cliente-list"),
    path("clientes/novo/", views.ClienteCreateView.as_view(), name="cliente-create"),
    path("clientes/<int:pk>/editar/", views.ClienteUpdateView.as_view(), name="cliente-update"),
    path("clientes/<int:pk>/excluir/", views.ClienteDeleteView.as_view(), name="cliente-delete"),
    path("veiculos/", views.VeiculoListView.as_view(), name="veiculo-list"),
    path("veiculos/novo/", views.VeiculoCreateView.as_view(), name="veiculo-create"),
    path("veiculos/<int:pk>/editar/", views.VeiculoUpdateView.as_view(), name="veiculo-update"),
    path("veiculos/<int:pk>/excluir/", views.VeiculoDeleteView.as_view(), name="veiculo-delete"),
    path("servicos/", views.ServicoListView.as_view(), name="servico-list"),
    path("servicos/novo/", views.ServicoCreateView.as_view(), name="servico-create"),
    path("servicos/<int:pk>/editar/", views.ServicoUpdateView.as_view(), name="servico-update"),
    path("servicos/<int:pk>/excluir/", views.ServicoDeleteView.as_view(), name="servico-delete"),
    path("orcamentos/", views.orcamento_list, name="orcamento-list"),
    path("orcamentos/novo/", views.orcamento_create, name="orcamento-create"),
    path("orcamentos/<int:pk>/status/", views.orcamento_status, name="orcamento-status"),
]
