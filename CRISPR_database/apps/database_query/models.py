from django.db import models

# Create your models here.
# from django.contrib.auth.models import AbstractUser


class CRISPR(models.Model):
    '''
    CRISPR 类型选择 一共十种
    '''

    CRISPR_Type_Choices = (
        ('I','第一种类型'),
        ('II','第二种类型'),
        ('III', '第三种类型'),
        ('IV', '第四种类型'),
        ('V', '第五种类型'),
        ('VI', '第六种类型'),
        ('VII', '第七种类型'),
        ('VIII', '第八种类型'),
        ('IX', '第九种类型'),
        ('X', '第十种类型'),

    )

    index = models.AutoField(primary_key=True,blank=False,verbose_name='PK')
    CRISPR_Consensus = models.TextField(null = True, blank = True, verbose_name= "CRISPR 序列")
    CRISPR_name = models.CharField(ｍａx_length = 50,null = True, blank = True,verbose_name='CRISPR 名字')
    CRISPR_Length = models.IntegerField(null = True,blank=True,verbose_name='the length of CRISPR')
    Organism = models.CharField(max_length=100,blank=True, null=True, verbose_name='the source of bacterial')
    CRISPR_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='CRISPR types ',
                                   choices=CRISPR_Type_Choices)
    PI_Sequence = models.TextField(null = True, blank = True, verbose_name= "PI sequences")
    PI_Length = models.IntegerField(null=True, blank=True, verbose_name="the length of PI")
    PI_Start_Position = models.IntegerField(null=True,blank=True,verbose_name='the start position of PI_sequences in CRISPR_sequence')
    PAM_Consensus = models.CharField(max_length=50,null = True, blank = True, verbose_name= 'PAM 序列')
    PAM_Length = models.IntegerField(null=True,blank=True,verbose_name='the length of PAM')

    # class Meta:
    #     verbose_name = 'CRISPR' #备注数据名称
    #     verbose_name_plural = verbose_name
    #
    # def __str__(self):
    #     return self.name