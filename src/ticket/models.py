# encoding=utf-8

import uuid

from django.db import models
from django.core.urlresolvers import reverse


class Sponsor(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "スポンサー"
        ordering = ("id",)

    CATEGORY_OWNER = "owner"
    CATEGORY_CROSS = "cross"
    CATEGORY_PLATINUM = "platinum"
    CATEGORY_GOLD = "gold"
    CATEGORY_SILVER = "silver"
    CATEGORY_IRON = "iron"
    CATEGORY_COMMUNITY = "community"
    CATEGORY_POWER = "power"
    CATEGORY_SPEAKER = "speaker"
    CATEGORY_CHOICES = (
        (CATEGORY_OWNER, "主催"),
        (CATEGORY_CROSS, "CROSS"),
        (CATEGORY_PLATINUM, "プラチナ"),
        (CATEGORY_GOLD, "ゴールド"),
        (CATEGORY_SILVER, "シルバー"),
        (CATEGORY_IRON, "アイアン"),
        (CATEGORY_COMMUNITY, "コミュニティ"),
        (CATEGORY_SPEAKER, "登壇者")
    )

    name = models.CharField("名称", max_length=100)
    shimei = models.CharField("担当者氏名", max_length=100)
    email = models.EmailField("メールアドレス", blank=True)
    category = models.CharField("スポンサー種別", max_length=50, choices=CATEGORY_CHOICES)
    token = models.CharField("トークン", max_length=100, unique=True)
    is_enabled = models.BooleanField("有効", default=True, blank=True)
    description = models.TextField("備考", blank=True)

    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.token:
            self.token = str(uuid.uuid4())

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("sponsor_detail", args=(self.id,))

    def get_default_ticket_count(self):
        master = {
            self.CATEGORY_OWNER: 20,
            self.CATEGORY_CROSS: 5,
            self.CATEGORY_PLATINUM: 15,
            self.CATEGORY_GOLD: 10,
            self.CATEGORY_SILVER: 5,
            self.CATEGORY_IRON: 3,
            self.CATEGORY_COMMUNITY: 3,
            self.CATEGORY_SPEAKER: 1
        }
        return master.get(self.category, 0)

    def is_in_preparation(self):
        return self.tickets.filter(is_registered=False).count() > 0


class Account(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "Ptxアカウント"
        ordering = ("id",)

    name = models.CharField("表示名", max_length=100)
    email = models.EmailField("メールアドレス", max_length=300)
    password = models.CharField("パスワード", max_length=50)
    is_registered = models.BooleanField("登録済", blank=True, default=False)

    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = "購入済みチケット"
        ordering = ("sponsor", "is_booth", "id",)

    name = models.CharField("チケット名", max_length=100, blank=True)
    sponsor = models.ForeignKey("Sponsor", verbose_name="スポンサー", related_name="tickets")
    account = models.OneToOneField("Account", verbose_name="Ptxアカウント", blank=True, null=True)
    qr_code = models.ImageField("QRコード", upload_to="qr", blank=True)
    is_registered = models.BooleanField("購入済", blank=True, default=False)

    # 参加者情報
    is_booth = models.BooleanField("ブース担当者", default=False, blank=True)
    shimei = models.CharField("氏名", max_length=100, blank=True)

    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)

    def __str__(self):
        return self.name
