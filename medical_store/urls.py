from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import (
    CountAPI,
    ExpiryAPI,
    StockAPI,
    MedicineInventoryViewSets,
    CompanyDetailsViewSets,
    PurchaseViewSets,
    SalesViewSets,
)

app_name = "medical_store"

# router = SimpleRouter()
# router.register("medicine-inventory", views.MedicineInventoryViewSets, basename="api-medical-inventory")
# router.register("company_details", views.CompanyDetailsViewSets, basename="api-company-details")
# #router.register("purchase", views.PurchaseViewSets, basename="api-purchase")
# #router.register("purchase-inventory", views.PurchaseInventoryViewSets, basename="api-purchase-inventory")
# #router.register("sales", views.SalesViewSets, basename="api-sales")
# #router.register("sales-inventory", views.SalesInventoryViewSets, basename="api-sales-inventory")

# urlpatterns = router.urls
urlpatterns = [
    path("count/", CountAPI.as_view(), name="count-API"),
    path("expiry/", ExpiryAPI.as_view(), name="expiry-API"),
    path("stock/", StockAPI.as_view(), name="stock-API"),
]

router = SimpleRouter()
router.register(
    "medicine-inventory",
    MedicineInventoryViewSets,
    basename="api-medical-inventory",
)
router.register(
    "company_details", CompanyDetailsViewSets, basename="api-company-details"
)
router.register("purchase", PurchaseViewSets, basename="api-purchase")
# router.register("purchase-inventory", views.PurchaseInventoryViewSets, basename="api-purchase-inventory")
router.register("sales", SalesViewSets, basename="api-sales")
# router.register("sales-inventory", views.SalesInventoryViewSets, basename="api-sales-inventory")

urlpatterns = urlpatterns + router.urls
