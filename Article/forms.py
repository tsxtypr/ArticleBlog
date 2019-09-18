from django import forms

class Test(forms.Form):
    name=forms.CharField(max_length=8,required=True)
    password=forms.CharField(max_length=8,required=True)

    def clean_name(self):
        # 获得name这条字段
        name=self.cleaned_data.get('name')
        # 判断这条字段
        if name=='admin':
            # 如果这条字段是admin,则不可以进行输入
            self.add_error('name','不可以是admin')
        else:
            # 其他的情况则会正常返回这个名字
            return name