import string
import random

from django.db import models


# ---------------------------------------------------------------------------
# Anatomy / sampling context
# ---------------------------------------------------------------------------
class Tissue(models.Model):
    """Anatomical origin of a sample (renamed from the old `Sublocation`)."""

    organ = models.CharField(max_length=255, blank=True)
    structure = models.CharField(max_length=255, blank=True)
    uberon_id = models.CharField(max_length=255, blank=True)  # UBERON ontology ID

    def __str__(self):
        return f"{self.organ} - {self.structure}"

    class Meta:
        verbose_name = "Tissue"
        verbose_name_plural = "Tissues"


class OntogenicStage(models.Model):
    """Developmental / life stage of the organism (renamed from `StageOfLife`)."""

    stage = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.stage} - {self.age}"

    class Meta:
        verbose_name = "Ontogenic stage"
        verbose_name_plural = "Ontogenic stages"


class ModelSpecies(models.Model):
    """
    A species-in-context record.

    The old standalone `Species` model has been merged into this table, so the
    species name / taxID now live here directly instead of via a ForeignKey.

    The links to Tissue and Ontogenic stage are one-to-one (per the diagram)
    and now optional. on_delete is SET_NULL so that deleting a Tissue/Stage
    leaves the species record intact (with an empty link) rather than deleting
    it — safer for a reference dataset. Switch back to CASCADE if you'd rather
    a deletion remove the whole record.
    """

    species_name = models.CharField(max_length=255, blank=True)
    species_taxid = models.CharField(max_length=255, blank=True)
    taxid = models.CharField(max_length=255, blank=True)  # NOTE: looks redundant with species_taxid

    tissue = models.OneToOneField(
        Tissue, on_delete=models.SET_NULL, null=True, blank=True
    )  # O2O per diagram, optional
    stage = models.OneToOneField(
        OntogenicStage, on_delete=models.SET_NULL, null=True, blank=True
    )  # O2O per diagram, optional

    def __str__(self):
        return f"{self.species_name} - {self.tissue} - {self.stage}"

    class Meta:
        verbose_name = "Model Species"
        verbose_name_plural = "Model Species"


# ---------------------------------------------------------------------------
# Glycan-related models
# ---------------------------------------------------------------------------
class MonosaccharideComposition(models.Model):
    """Composition of a glycan in terms of its monosaccharide content."""

    # Counts default to 0, so "none" is already represented — left as-is.
    H_num = models.PositiveIntegerField(default=0)  # Hexose (Glc, Gal, Man)
    N_num = models.PositiveIntegerField(default=0)  # N-acetylhexosamine (GlcNAc, GalNAc)
    F_num = models.PositiveIntegerField(default=0)  # Fucose
    P_num = models.PositiveIntegerField(default=0)  # Phosphate
    T_num = models.PositiveIntegerField(default=0)  # Sulphate
    G_num = models.PositiveIntegerField(default=0)  # Neu5Gc
    S_num = models.PositiveIntegerField(default=0)  # Neu5Ac
    E_num = models.PositiveIntegerField(default=0)  # Neu5Ac EE (ethyl esterification)
    M_num = models.PositiveIntegerField(default=0)  # Neu5Ac MA (methyl amidation)
    # NOTE: A_num (GlcA) has been removed — it is not present in the new diagram.

    composition_string = models.CharField(
        max_length=255, editable=False, blank=True
    )  # Auto-generated composition string

    def __str__(self):
        return self.composition_string

    def save(self, *args, **kwargs):
        # Build the composition string in a stable, defined order.
        elements = []
        for letter, value in (
            ("H", self.H_num),
            ("N", self.N_num),
            ("F", self.F_num),
            ("P", self.P_num),
            ("T", self.T_num),
            ("G", self.G_num),
            ("S", self.S_num),
            ("E", self.E_num),
            ("M", self.M_num),
        ):
            if value > 0:
                elements.append(f"{letter}{value}")
        self.composition_string = "".join(elements)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Monosaccharide composition"
        verbose_name_plural = "Monosaccharide compositions"


class LastAuthor(models.Model):
    """Details about the last author of a study."""

    full_name = models.CharField(max_length=255, blank=True)
    affiliation = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Last author"
        verbose_name_plural = "Last authors"


class Study(models.Model):
    """A research study including publication details."""

    title = models.CharField(max_length=255, blank=True)
    journal = models.CharField(max_length=255, blank=True)
    year = models.IntegerField(null=True, blank=True)
    # null=True + unique=True: in Postgres multiple NULLs don't clash, so several
    # studies with no DOI yet can coexist. (Don't use blank '' here, or the second
    # empty DOI would violate the unique constraint.)
    doi = models.CharField(max_length=255, unique=True, null=True, blank=True)
    last_authors = models.ManyToManyField(LastAuthor, related_name="studies", blank=True)  # M2M

    def __str__(self):
        return f"{self.title} | {self.journal} | {self.year} | DOI: {self.doi}"

    class Meta:
        verbose_name = "Study"
        verbose_name_plural = "Studies"


# Generates a unique glycan ID in the format LBG-xxxxx
def generate_unique_glycan_id():
    while True:
        glycan_id = f"LBG-{''.join(random.choices(string.ascii_uppercase + string.digits, k=5))}"
        if not Glycan.objects.filter(id=glycan_id).exists():
            return glycan_id


class Glycan(models.Model):
    """A glycan with structural, mass, cross-reference, and study data."""

    # Human-readable LBG-xxxxx public ID (kept from the original).
    id = models.CharField(max_length=9, primary_key=True, editable=False, unique=True)

    # External database cross-references
    glytoucan_id = models.CharField(max_length=255, blank=True)
    glycosmos_id = models.CharField(max_length=255, blank=True)
    glyconnect_id = models.CharField(max_length=255, blank=True)
    wurcs = models.TextField(blank=True)  # WURCS strings can get long, so TextField

    brain_specific = models.BooleanField(default=False)

    # SNFG, static image (was `structural_resolution`)
    graphical_structure = models.ImageField(upload_to="images/", null=True, blank=True)

    mass = models.FloatField(null=True, blank=True)
    theoretical_mass = models.FloatField(null=True, blank=True)
    sialic_acid_derivatization = models.BooleanField(default=False)  # was `sialic_derivatization`

    gu_mean = models.FloatField(null=True, blank=True)
    gu_max = models.FloatField(null=True, blank=True)
    gu_min = models.FloatField(null=True, blank=True)

    monosaccharide_comp = models.ForeignKey(
        MonosaccharideComposition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="glycans",
    )  # O2M, optional (SET_NULL so deleting a composition keeps the glycan)
    model_species = models.ManyToManyField(ModelSpecies, blank=True)  # M2M
    studies = models.ManyToManyField(Study, blank=True)               # M2M
    # NOTE: the DiagnosticFragment model + its M2M have been removed — they are
    # not present in the new diagram.

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_glycan_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Glycan {self.id}"

    class Meta:
        verbose_name = "Glycan"
        verbose_name_plural = "Glycans"
