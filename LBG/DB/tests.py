from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from .models import Glycan, MonosaccharideComposition
from .admin import GlycanAdmin, GURangeFilter

class GURangeFilterTest(TestCase):
    def setUp(self):
        # Create test MonosaccharideComposition
        comp = MonosaccharideComposition.objects.create(H_num=2)
        # Create Glycans in different GU ranges
        Glycan.objects.create(id="LBG-A0001", monosaccharide_comp=comp, mass=1000, gu_mean=1.5, gu_min=1.0, gu_max=2.0)
        Glycan.objects.create(id="LBG-A0002", monosaccharide_comp=comp, mass=1000, gu_mean=3.0, gu_min=2.0, gu_max=4.0)
        Glycan.objects.create(id="LBG-A0003", monosaccharide_comp=comp, mass=1000, gu_mean=8.0, gu_min=7.0, gu_max=9.0)

    def test_filter_gu_range(self):
        request = RequestFactory().get('/')
        filter_instance = GURangeFilter(request, {}, Glycan, GlycanAdmin)
        queryset = Glycan.objects.all()
        
        filter_instance.value = lambda: "2-5"
        filtered = filter_instance.queryset(request, queryset)
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first().gu_mean, 3.0)
