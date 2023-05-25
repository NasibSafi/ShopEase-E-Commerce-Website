# Generated by Django 4.0.4 on 2022-06-30 08:30

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='商品SPU名称')),
                ('detail', tinymce.models.HTMLField(blank=True, verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
                'db_table': 'f_goods_spu',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('desc', models.CharField(max_length=256, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('unite', models.CharField(max_length=20, verbose_name='单位')),
                ('image', models.ImageField(upload_to='goods', verbose_name='商品图片')),
                ('stock', models.IntegerField(default=1, verbose_name='库存')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('state', models.SmallIntegerField(choices=[(0, '下架'), (1, '上架')], default=1, verbose_name='商品状态')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品SPU')),
            ],
            options={
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
                'db_table': 'f_goods_sku',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='种类名称')),
                ('logo', models.CharField(max_length=20, verbose_name='标识')),
                ('image', models.ImageField(upload_to='type', verbose_name='商品类型图片')),
            ],
            options={
                'verbose_name': '商品种类表',
                'verbose_name_plural': '商品种类表',
                'db_table': 'f_goods_type',
            },
        ),
        migrations.CreateModel(
            name='IndexPromotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='活动名称')),
                ('url', models.CharField(max_length=256, verbose_name='活动链接')),
                ('image', models.ImageField(upload_to='index', verbose_name='活动图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
            ],
            options={
                'verbose_name': '首页活动表',
                'verbose_name_plural': '首页活动表',
                'db_table': 'f_index_promotion',
            },
        ),
        migrations.CreateModel(
            name='IndexGoodsBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='删除标记')),
                ('image', models.ImageField(upload_to='index', verbose_name='轮播图图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodssku', verbose_name='商品id')),
            ],
            options={
                'verbose_name': '首页轮播图表',
                'verbose_name_plural': '首页轮播图表',
                'db_table': 'f_index_banner',
            },
        ),
        migrations.CreateModel(
            name='IndexCreatoryGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='删除标记')),
                ('display_mode', models.SmallIntegerField(choices=[(0, '标题'), (1, '图片')], default=1, verbose_name='展示模式')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodssku', verbose_name='商品id')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodstype', verbose_name='商品种类id')),
            ],
            options={
                'verbose_name': '首页分类商品表',
                'verbose_name_plural': '首页分类商品表',
                'db_table': 'f_index_creatory',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodstype', verbose_name='关联的商品种类'),
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='删除标记')),
                ('path', models.ImageField(upload_to='goods', verbose_name='图片路径')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodssku', verbose_name='商品sku关联的id')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
                'db_table': 'f_goods_image',
            },
        ),
    ]
