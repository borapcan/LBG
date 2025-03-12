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


# Admin configuration for Species model
@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# Admin configuration for StageOfLife model
@admin.register(StageOfLife)
class StageOfLifeAdmin(admin.ModelAdmin):
    list_display = ("id", "stage", "age")
    search_fields = ("stage", "age")


# Admin configuration for Sublocation model
@admin.register(Sublocation)
class SublocationAdmin(admin.ModelAdmin):
    list_display = ("id", "organ", "structure")
    search_fields = ("organ", "structure")


# Admin configuration for ModelSpecies model
@admin.register(ModelSpecies)
class ModelSpeciesAdmin(admin.ModelAdmin):
    list_display = ("id", "species", "sublocation", "stage_of_life")
    search_fields = ("species__name", "sublocation__organ", "stage_of_life__stage")
    list_filter = ("species", "stage_of_life")


# Admin configuration for MonosaccharideComposition model
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
        "__str__",  # Displays the computed composition string
    )
    search_fields = ("composition_string",)


# Admin configuration for DiagnosticFragment model
@admin.register(DiagnosticFragment)
class DiagnosticFragmentAdmin(admin.ModelAdmin):
    list_display = ("id", "motif_name", "mass")
    search_fields = ("motif_name", "mass")


# Admin configuration for LastAuthor model
@admin.register(LastAuthor)
class LastAuthorAdmin(admin.ModelAdmin):
    search_fields = ("full_name", "affiliation")


# Admin configuration for Study model
@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "journal", "year", "doi", "authors_list")
    search_fields = ("title", "journal", "doi", "last_authors__full_name")
    list_filter = ("year", "journal")
    autocomplete_fields = ["last_authors"]

    def authors_list(self, obj):
        """Displays a comma-separated list of authors for the study."""
        return ", ".join(author.full_name for author in obj.last_authors.all())

    authors_list.short_description = "Authors"


# Custom filter for filtering Glycan records based on associated species
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


# Custom filter for filtering Glycan records by Glycan Unit (GU) range
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
        if self.value():
            min_val, max_val = {
                "0-2": (0.0, 2.0),
                "2-5": (2.0, 5.0),
                "5-7": (5.0, 7.0),
                "7-10": (7.0, 10.0),
                "10+": (10.0, None),
            }.get(self.value(), (None, None))

            if min_val is not None and max_val is not None:
                return queryset.filter(gu_mean__gte=min_val, gu_mean__lt=max_val)
            elif min_val is not None:
                return queryset.filter(gu_mean__gte=min_val)
        return queryset


# Custom filter for filtering Glycan records by mass range
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
        if self.value():
            min_val, max_val = {
                "0-500": (0, 500),
                "500-1000": (500, 1000),
                "1000-1500": (1000, 1500),
                "1500-2000": (1500, 2000),
                "2000+": (2000, None),
            }.get(self.value(), (None, None))

            if min_val is not None and max_val is not None:
                return queryset.filter(mass__gte=min_val, mass__lt=max_val)
            elif min_val is not None:
                return queryset.filter(mass__gte=min_val)
        return queryset


# Admin configuration for Glycan model
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
    search_fields = ("monosaccharide_comp__composition_string",)
    list_filter = (
        "sialic_derivatization",
        GURangeFilter,
        MassRangeFilter,
    )
    filter_horizontal = ("model_species", "studies", "diagnostic_fragments")

    def monosaccharide_composition_display(self, obj):
        """Displays the composition string of the associated MonosaccharideComposition."""
        return str(obj.monosaccharide_comp)

    monosaccharide_composition_display.short_description = "Monosaccharide Composition"

    def display_image(self, obj):
        """Displays a thumbnail of the glycan's structural resolution image."""
        if obj.structural_resolution:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:contain;"/>',
                obj.structural_resolution.url,
            )
        return "No Image"

    display_image.short_description = "Structure Image"
