from django.db import models

# Create your models here.


class BannerImages(models.Model):

    title = models.CharField(verbose_name="عنوان بنر", max_length=100, default="")
    subtitle = models.CharField(verbose_name="زیر عنوان", max_length=100, default="")
    image = models.ImageField(verbose_name="بنر صفحه اصلی", upload_to="images/banners")

    def __str__(self):
        return f"{self.title} --> {self.subtitle}"

    class Meta:
        verbose_name = "بنر صفحه اصلی"
        verbose_name_plural = "بنر های صفحه اصلی"


class Header(models.Model):
    title = models.CharField(verbose_name="عنوان هدر", max_length=20)
    url = models.CharField(verbose_name="لینک", null=True, blank=True, max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "هدر"
        verbose_name_plural = "هدر ها"
        ordering = ["order"]

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    site_name = models.CharField(verbose_name="نام سایت", max_length=100)
    site_logo = models.ImageField(
        verbose_name="لوگوی سایت", upload_to="images/site-setting"
    )
    title = models.CharField(
        verbose_name="عنوان درباره ما", max_length=100, default="درباره ما"
    )
    text = models.TextField(verbose_name="متن درباره ما صفحه اصلی")
    imageurl = models.ImageField(
        verbose_name="عکس درباره ما صفحه اصلی", upload_to="images/site-setting"
    )
    phone = models.CharField(verbose_name="تلفن", max_length=20)
    email = models.CharField(verbose_name="ایمیل", max_length=60)
    address = models.CharField(verbose_name="آدرس", max_length=200)

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات"

    def __str__(self):
        return self.site_name


class FooterLinkBox(models.Model):
    title = models.CharField(verbose_name="عنوان دسته بندی لینک", max_length=40)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی لینک فوتر"
        verbose_name_plural = "دسته بندی های لینک فوتر"


class FooterLink(models.Model):
    title = models.CharField(verbose_name="دسته بندی لینک", max_length=40)
    url = models.CharField(verbose_name="لینک", null=True, blank=True, max_length=100)
    footer_link_box = models.ForeignKey(
        FooterLinkBox,
        on_delete=models.CASCADE,
        verbose_name="دسته بندی",
        related_name="footer_link",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "لینک فوتر"
        verbose_name_plural = "لینک های فوتر"


class TrustSymbols(models.Model):
    image = models.ImageField(
        verbose_name="عکس نماد اعتماد", upload_to="images/trust-symbol"
    )

    class Meta:
        verbose_name = "نماد اعتماد"
        verbose_name_plural = "نماد های اعتماد"


class ContactUsInfo(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    telegram = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=255)
    work_hours = models

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class ContactUsMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField(max_length=1024)