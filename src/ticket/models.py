# encoding=utf-8

from django.db import models


class Sponsor(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "スポンサー"
        ordering = ("id",)

    CATEGORY_PLATINUM = "platinum"
    CATEGORY_GOLD = "gold"
    CATEGORY_SILVER = "silver"
    CATEGORY_IRON = "iron"
    CATEGORY_LUNCH = "lunch"
    CATEGORY_CHOICES = (
        (CATEGORY_PLATINUM, "プラチナ"),
        (CATEGORY_GOLD, "ゴールド"),
        (CATEGORY_SILVER, "シルバー"),
        (CATEGORY_IRON, "アイアン"),
        (CATEGORY_LUNCH, "ランチ"),
    )

    name = models.CharField("名称", max_length=100)
    shimei = models.CharField("担当者氏名", max_length=100)
    email = models.EmailField("メールアドレス", blank=True)
    category = models.IntegerField("スポンサー種別", choices=CATEGORY_CHOICES)
    token = models.CharField("トークン", max_length=100, unique=True)
    is_enabled = models.BooleanField("有効", default=True, blank=True)
    description = models.TextField("備考", blank=True)

    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)


class Account(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "Ptxアカウント"
        ordering = ("id",)

    name = models.CharField("名前", max_length=100)
    email = models.EmailField("メールアドレス", max_length=300)
    password = models.CharField("パスワード", max_length=50)
    is_registered = models.BooleanField("登録済", blank=True, default=False)

    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)


class Ticket(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "購入済みチケット"
        ordering = ("id",)

    name = models.CharField("チケット名", max_length=100, blank=True)
    sponsor = models.ForeignKey("Sponsor", verbose_name="スポンサー")
    account = models.OneToOneField("Account", verbose_name="Ptxアカウント", blank=True, null=True)
    qr_code = models.ImageField("QRコード", upload_to="qr", blank=True)
    is_registered = models.BooleanField("購入済", blank=True, default=False)

    # 参加者情報
    is_booth = models.BooleanField("ブース担当者", default=False, blank=True)
    shimei = models.CharField("氏名", max_length=100, blank=True)

    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)
