# Generated by Django 2.1 on 2019-06-09 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
            ],
            options={
                'verbose_name': '成绩',
                'verbose_name_plural': '成绩',
                'db_table': 'grade',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='', max_length=20, verbose_name='科目')),
                ('major', models.CharField(max_length=20, verbose_name='考卷适用专业')),
                ('examtime', models.DateTimeField()),
            ],
            options={
                'verbose_name': '试卷',
                'verbose_name_plural': '试卷',
                'db_table': 'paper',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=20, verbose_name='科目')),
                ('title', models.TextField(verbose_name='题目')),
                ('optionA', models.CharField(max_length=30, verbose_name='A选项')),
                ('optionB', models.CharField(max_length=30, verbose_name='B选项')),
                ('optionC', models.CharField(max_length=30, verbose_name='C选项')),
                ('optionD', models.CharField(max_length=30, verbose_name='D选项')),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=10,
                                            verbose_name='答案')),
                ('level', models.CharField(choices=[('2', 'general'), ('3', 'difficult'), ('1', 'easy')], max_length=10,
                                           verbose_name='等级')),
                ('score', models.IntegerField(default=1, verbose_name='分数')),
            ],
            options={
                'verbose_name': '单项选择题库',
                'verbose_name_plural': '单项选择题库',
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='学号')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('sex',
                 models.CharField(choices=[('男', '男'), ('女', '女')], default='男', max_length=4, verbose_name='性别')),
                ('dept', models.CharField(
                    choices=[('计算机与通信学院', '计算机与通信学院'), ('电气与自动化学院', '电气与自动化学院'), ('外国语学院', '外国语学院'), ('理学院', '理学院')],
                    default=None, max_length=20, verbose_name='学院')),
                ('major', models.CharField(default=None, max_length=20, verbose_name='专业')),
                ('password', models.CharField(default='111', max_length=20, verbose_name='密码')),
                ('email', models.EmailField(default=None, max_length=254, verbose_name='邮箱')),
                ('birth', models.DateField(verbose_name='出生日期')),
            ],
            options={
                'verbose_name': '学生',
                'verbose_name_plural': '学生',
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='教工号')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('sex',
                 models.CharField(choices=[('男', '男'), ('女', '女')], default='男', max_length=4, verbose_name='性别')),
                ('dept', models.CharField(
                    choices=[('计算机与通信学院', '计算机与通信学院'), ('电气与自动化学院', '电气与自动化学院'), ('外国语学院', '外国语学院'), ('理学院', '理学院')],
                    default=None, max_length=20, verbose_name='学院')),
                ('email', models.EmailField(default=None, max_length=254, verbose_name='邮箱')),
                ('password', models.CharField(default='000000', max_length=20, verbose_name='密码')),
                ('birth', models.DateField(verbose_name='出生日期')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
                'db_table': 'teacher',
            },
        ),
        migrations.AddField(
            model_name='paper',
            name='pid',
            field=models.ManyToManyField(to='student.Question'),
        ),
        migrations.AddField(
            model_name='paper',
            name='tid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Teacher'),
        ),
        migrations.AddField(
            model_name='grade',
            name='sid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
    ]
