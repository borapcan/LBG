from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Species,
    StageOfLife,
    Sublocation,
    ModelSpecies,
    MonosaccharideComponent,
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


# Monosaccharide Component Admin
@admin.register(MonosaccharideComponent)
class MonosaccharideComponentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "h_num",
        "n_num",
        "f_num",
        "sg_num",
        "sn_num",
        "phos_num",
        "sulph_num",
        "unmod_sia",
    )
    search_fields = (
        "h_num",
        "n_num",
        "f_num",
        "sg_num",
        "sn_num",
        "phos_num",
        "sulph_num",
        "unmod_sia",
    )


# Diagnostic Fragment Admin
@admin.register(DiagnosticFragment)
class DiagnosticFragmentAdmin(admin.ModelAdmin):
    list_display = ("id", "motif_name", "motif_structure")
    search_fields = ("motif_name", "motif_structure")


# Diagnostic Fragment Admin
@admin.register(LastAuthor)
class LastAuthorAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "affiliation")


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "journal", "year", "doi")
    search_fields = ("title", "journal", "doi")
    list_filter = ("year", "journal")

    # Option 1: Dropdown search with add button
    autocomplete_fields = ["last_authors"]


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


@admin.register(Glycan)
class GlycanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "glycan_name_comp",
        "mass",
        "sialic_derivatization",
        "gu_mean",
        "gu_max",
        "gu_min",
        "display_image",
    )
    search_fields = ("model_species__species__name",)
    list_filter = ("sialic_derivatization",)
    filter_horizontal = ("model_species", "studies", "diagnostic_fragments")

    def display_image(self, obj):
        if obj.structural_resolution:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:contain;"/>',
                obj.structural_resolution.url,
            )
        return "No Image"

    display_image.short_description = "Structure Image"
