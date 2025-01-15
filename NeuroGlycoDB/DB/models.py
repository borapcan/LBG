from django.db import models


## species section
class Species(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"


class StageOfLife(models.Model):
    stage = models.CharField(max_length=255)
    age = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.stage} - {self.age}"

    class Meta:
        verbose_name = "Stage of Life"
        verbose_name_plural = "Stages of Life"


class Sublocation(models.Model):
    organ = models.CharField(max_length=255)
    structure = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.organ} - {self.structure}"

    class Meta:
        verbose_name = "Sublocation"
        verbose_name_plural = "Sublocations"


class ModelSpecies(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    sublocation = models.OneToOneField(Sublocation, on_delete=models.CASCADE)
    stage_of_life = models.OneToOneField(StageOfLife, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.species.name} - {self.sublocation} - {self.stage_of_life}"

    class Meta:
        verbose_name = "Model Species"
        verbose_name_plural = "Model Species"  # No 'Model Speciess'


# glycan part


class MonosaccharideComponent(models.Model):
    h_num = models.IntegerField()
    n_num = models.IntegerField()
    f_num = models.IntegerField()
    sg_num = models.IntegerField()
    sn_num = models.IntegerField()
    phos_num = models.IntegerField()
    sulph_num = models.IntegerField()
    unmod_sia = models.IntegerField()

    def __str__(self):
        return f"H:{self.h_num} N:{self.n_num} F:{self.f_num}"

    class Meta:
        verbose_name = "Monosaccharide Component"
        verbose_name_plural = "Monosaccharide Components"


class DiagnosticFragment(models.Model):
    motif_name = models.CharField(max_length=255)
    motif_structure = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.motif_name

    class Meta:
        verbose_name = "Diagnostic Fragment"
        verbose_name_plural = "Diagnostic Fragments"


class Study(models.Model):
    title = models.CharField(max_length=255)
    journal = models.CharField(max_length=255)
    year = models.IntegerField()
    doi = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Study"
        verbose_name_plural = "Studies"


class LastAuthor(models.Model):
    full_name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)
    study = models.ForeignKey(
        Study, related_name="last_authors", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Last Author"
        verbose_name_plural = "Last Authors"


class Glycan(models.Model):
    structural_resolution = models.TextField(
        null=True, blank=True
    )  # For SMILES or similar
    # graphical_structure = models.TextField(null=True, blank=True)  # SNFG or image URL
    monosaccharide_comp = models.OneToOneField(
        MonosaccharideComponent, on_delete=models.CASCADE
    )
    mass = models.FloatField()
    sialic_derivatization = models.BooleanField(default=False)
    gu_mean = models.FloatField()
    gu_max = models.FloatField()
    gu_min = models.FloatField()

    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    model_species = models.ManyToManyField(ModelSpecies)
    studies = models.ManyToManyField(Study)
    diagnostic_fragments = models.ManyToManyField(DiagnosticFragment)

    def __str__(self):
        return f"Glycan {self.id}"

    class Meta:
        verbose_name = "Glycan"
        verbose_name_plural = "Glycans"
