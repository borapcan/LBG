import string, random
from django.db import models


## Species section
class Species(models.Model):
    # Represents different species in the database
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"


class StageOfLife(models.Model):
    # Represents different life stages of a species
    stage = models.CharField(max_length=255)
    age = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.stage} - {self.age}"

    class Meta:
        verbose_name = "Stage of Life"
        verbose_name_plural = "Stages of Life"


class Sublocation(models.Model):
    # Represents anatomical sublocations within a species
    organ = models.CharField(max_length=255)
    structure = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.organ} - {self.structure}"

    class Meta:
        verbose_name = "Sublocation"
        verbose_name_plural = "Sublocations"


class ModelSpecies(models.Model):
    # Links species to a specific sublocation and life stage
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    sublocation = models.ForeignKey(Sublocation, on_delete=models.CASCADE)
    stage_of_life = models.ForeignKey(StageOfLife, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.species.name} - {self.sublocation} - {self.stage_of_life}"

    class Meta:
        verbose_name = "Model Species"
        verbose_name_plural = "Model Species"


## Glycan-related models
class MonosaccharideComposition(models.Model):
    # Stores the composition of a glycan in terms of its monosaccharide content
    H_num = models.PositiveIntegerField(default=0)  # Hexose (Glu, Gal, Man)
    N_num = models.PositiveIntegerField(
        default=0
    )  # N-acetylhexosamine (GlcNAc, GalNAc)
    F_num = models.PositiveIntegerField(default=0)  # Fucose
    P_num = models.PositiveIntegerField(default=0)  # Phosphate
    T_num = models.PositiveIntegerField(default=0)  # Sulphate
    A_num = models.PositiveIntegerField(default=0)  # GlcA
    G_num = models.PositiveIntegerField(default=0)  # Neu5Gc
    S_num = models.PositiveIntegerField(default=0)  # Neu5Ac
    E_num = models.PositiveIntegerField(default=0)  # Neu5Ac EE (ethyl esterification)
    M_num = models.PositiveIntegerField(default=0)  # Neu5Ac MA (methyl amidation)
    composition_string = models.CharField(
        max_length=255, editable=False, blank=True
    )  # Auto-generated composition string

    def __str__(self):
        return self.composition_string

    def save(self, *args, **kwargs):
        # Generates a string representation of the composition before saving
        elements = []
        if self.H_num > 0:
            elements.append(f"H{self.H_num}")
        if self.N_num > 0:
            elements.append(f"N{self.N_num}")
        if self.F_num > 0:
            elements.append(f"F{self.F_num}")
        if self.P_num > 0:
            elements.append(f"P{self.P_num}")
        if self.T_num > 0:
            elements.append(f"T{self.T_num}")
        if self.A_num > 0:
            elements.append(f"A{self.A_num}")
        if self.G_num > 0:
            elements.append(f"G{self.G_num}")
        if self.S_num > 0:
            elements.append(f"S{self.S_num}")
        if self.E_num > 0:
            elements.append(f"E{self.E_num}")
        if self.M_num > 0:
            elements.append(f"M{self.M_num}")
        self.composition_string = "".join(elements)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Composition"
        verbose_name_plural = "Compositions"


class DiagnosticFragment(models.Model):
    # Stores information about diagnostic fragments used in analysis
    motif_name = models.CharField(max_length=255)
    mass = models.FloatField(default=0.00)

    def __str__(self):
        return self.motif_name

    class Meta:
        verbose_name = "Diagnostic Fragment"
        verbose_name_plural = "Diagnostic Fragments"


class LastAuthor(models.Model):
    # Stores details about the last author of a study
    full_name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Last Author"
        verbose_name_plural = "Last Authors"


class Study(models.Model):
    # Represents a research study including publication details
    title = models.CharField(max_length=255)
    journal = models.CharField(max_length=255)
    year = models.IntegerField()
    doi = models.CharField(max_length=255, unique=True)
    last_authors = models.ManyToManyField(LastAuthor, related_name="studies")

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
    # Represents a glycan with structural, mass, and associated study data
    id = models.CharField(max_length=9, primary_key=True, editable=False, unique=True)
    structural_resolution = models.ImageField(
        upload_to="images/", null=True, blank=True
    )
    monosaccharide_comp = models.ForeignKey(
        "MonosaccharideComposition", on_delete=models.CASCADE, related_name="glycans"
    )
    mass = models.FloatField()
    sialic_derivatization = models.BooleanField(default=False)
    gu_mean = models.FloatField()
    gu_max = models.FloatField()
    gu_min = models.FloatField()

    model_species = models.ManyToManyField("ModelSpecies")
    studies = models.ManyToManyField("Study")
    diagnostic_fragments = models.ManyToManyField("DiagnosticFragment", blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_unique_glycan_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Glycan {self.id}"

    class Meta:
        verbose_name = "Glycan"
        verbose_name_plural = "Glycans"
