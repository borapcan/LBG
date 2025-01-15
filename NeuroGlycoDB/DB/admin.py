from django.contrib import admin

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
    search_fields = ("h_num", "n_num", "f_num")


# Diagnostic Fragment Admin
@admin.register(DiagnosticFragment)
class DiagnosticFragmentAdmin(admin.ModelAdmin):
    list_display = ("id", "motif_name")
    search_fields = ("motif_name",)


# Inline Last Author for Study
class LastAuthorInline(admin.TabularInline):
    model = LastAuthor
    extra = 1


# Study Admin
@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "journal", "year", "doi")
    search_fields = ("title", "journal", "doi")
    list_filter = ("year", "journal")
    inlines = [LastAuthorInline]


# Glycan Admin
@admin.register(Glycan)
class GlycanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "species",
        "mass",
        "sialic_derivatization",
        "gu_mean",
        "gu_max",
        "gu_min",
    )
    search_fields = ("species__name",)
    list_filter = ("species", "sialic_derivatization")
    filter_horizontal = ("model_species", "studies", "diagnostic_fragments")
