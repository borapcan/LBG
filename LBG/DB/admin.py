from django.contrib import admin
from django.db.models import F
from django.utils.html import format_html
from .models import (
    Species,
    StageOfLife,
    Sublocation,
    ModelSpecies,
    MonosaccharideComposition,
    DiagnosticFragment,
    Study,
    LastAuthor,
    Glycan,
)


# Species Admin
@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# Stage of Life Admin
@admin.register(StageOfLife)
class StageOfLifeAdmin(admin.ModelAdmin):
    list_display = ("id", "stage", "age")
    search_fields = ("stage", "age")


# Sublocation Admin
@admin.register(Sublocation)
class SublocationAdmin(admin.ModelAdmin):
    list_display = ("id", "organ", "structure")
    search_fields = ("organ", "structure")


# Model Species Admin
@admin.register(ModelSpecies)
class ModelSpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "species", "sublocation", "stage_of_life")
    search_fields = ("species__name", "sublocation__organ", "stage_of_life__stage")
    list_filter = ("species", "stage_of_life")


# Monosaccharide Composition Admin
@admin.register(MonosaccharideComposition)
class MonosaccharideCompositionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "H_num",
        "N_num",
        "F_num",
        "P_num",
        "T_num",
        "A_num",
        "G_num",
        "S_num",
        "E_num",
        "M_num",
        "__str__",
    )
    search_fields = (
        "H_num",
        "N_num",
        "F_num",
        "P_num",
        "T_num",
        "A_num",
        "G_num",
        "S_num",
        "E_num",
        "M_num",
        "composition_string",
    )


# Diagnostic Fragment Admin
@admin.register(DiagnosticFragment)
class DiagnosticFragmentAdmin(admin.ModelAdmin):
    list_display = ("id", "motif_name", "mass")
    search_fields = ("motif_name", "mass")


# Last Author Admin
@admin.register(LastAuthor)
class LastAuthorAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "affiliation")


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "journal", "year", "doi", "authors_list")
    search_fields = ("title", "journal", "doi", "last_authors__full_name")
    list_filter = ("year", "journal")
    autocomplete_fields = ["last_authors"]

    def authors_list(self, obj):
        # Join the full names of all authors related to the study
        return ", ".join(author.full_name for author in obj.last_authors.all())

    authors_list.short_description = "Authors"


# Custom Filter for Species via ModelSpecies
class SpeciesFilter(admin.SimpleListFilter):
    title = "Species"
    parameter_name = "species"

    def lookups(self, request, model_admin):
        species = Species.objects.all()
        return [(s.id, s.name) for s in species]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(model_species__species__id=self.value())
        return queryset


# Custom Filter for GU Range
class GURangeFilter(admin.SimpleListFilter):
    title = "GU Range"
    parameter_name = "gu_range"

    def lookups(self, request, model_admin):
        return [
            ("0-2", "0.0 - 2.0"),
            ("2-5", "2.0 - 5.0"),
            ("5-7", "5.0 - 7.0"),
            ("7-10", "7.0 - 10.0"),
            ("10+", "> 10.0"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "0-2":
            return queryset.filter(gu_mean__gte=0.0, gu_mean__lt=2.0)
        elif self.value() == "2-5":
            return queryset.filter(gu_mean__gte=2.0, gu_mean__lt=5.0)
        elif self.value() == "5-7":
            return queryset.filter(gu_mean__gte=5.0, gu_mean__lt=7.0)
        elif self.value() == "7-10":
            return queryset.filter(gu_mean__gte=7.0, gu_mean__lte=10.0)
        elif self.value() == "10+":
            return queryset.filter(gu_mean__gt=10.0)
        return queryset


# Custom Filter for Mass Range
class MassRangeFilter(admin.SimpleListFilter):
    title = "Mass Range"
    parameter_name = "mass_range"

    def lookups(self, request, model_admin):
        return [
            ("0-500", "0 - 500"),
            ("500-1000", "500 - 1000"),
            ("1000-1500", "1000 - 1500"),
            ("1500-2000", "1500 - 2000"),
            ("2000+", "> 2000"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "0-500":
            return queryset.filter(mass__gte=0, mass__lt=500)
        elif self.value() == "500-1000":
            return queryset.filter(mass__gte=500, mass__lt=1000)
        elif self.value() == "1000-1500":
            return queryset.filter(mass__gte=1000, mass__lt=1500)
        elif self.value() == "1500-2000":
            return queryset.filter(mass__gte=1500, mass__lt=2000)
        elif self.value() == "2000+":
            return queryset.filter(mass__gt=2000)
        return queryset


@admin.register(Glycan)
class GlycanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "monosaccharide_composition_display",
        "mass",
        "sialic_derivatization",
        "gu_mean",
        "gu_max",
        "gu_min",
        "display_image",
    )
    search_fields = (
        "monosaccharide_comp__H_num",
        "monosaccharide_comp__N_num",
        "monosaccharide_comp__F_num",
        "monosaccharide_comp__P_num",
        "monosaccharide_comp__T_num",
        "monosaccharide_comp__A_num",
        "monosaccharide_comp__G_num",
        "monosaccharide_comp__S_num",
        "monosaccharide_comp__E_num",
        "monosaccharide_comp__M_num",
        "monosaccharide_comp__composition_string",
    )
    list_filter = (
        "sialic_derivatization",
        GURangeFilter,
        MassRangeFilter,
    )
    filter_horizontal = ("model_species", "studies", "diagnostic_fragments")

    def monosaccharide_composition_display(self, obj):
        return str(obj.monosaccharide_comp)

    monosaccharide_composition_display.short_description = "Monosaccharide Composition"

    def display_image(self, obj):
        if obj.structural_resolution:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:contain;"/>',
                obj.structural_resolution.url,
            )
        return "No Image"

    display_image.short_description = "Structure Image"
