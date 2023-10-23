import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp,shapiro,levene,ttest_ind,mannwhitneyu,pearsonr,spearmanr,kendalltau,f_oneway,kruskal
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multicomp import MultiComparison

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',10)
pd.set_option('display.float_format', lambda x: '%.5f' %x)

control_group = pd.read_excel("datasets/ab_testing.xlsx",sheet_name='Control Group')
test_group = pd.read_excel("datasets/ab_testing.xlsx",sheet_name='Test Group')

control_group.groupby("Earning").agg({"Impression":"mean",
                                      "Click":"mean",
                                      "Purchase":"mean"}).sort_values("Earning",ascending=False)

control_group.describe().T
test_group.describe().T

test_group.sort_values("Earning",ascending=False)
control_group.sort_values("Earning",ascending=False) #Satın alma ,reklam görüntülenme kazanç artarken tıklanma sayısı azalıyor.


total_group = pd.concat([test_group,control_group]).reset_index()
total_group


test_group["Earning"].mean() #Test grubunun ortalaması 2514.8907326506173
control_group["Earning"].mean() #Control grubunun ortalaması 1908.568299802749

#Test ve control grubu arasında gözle görülür bir farklılık vardır.Fakat şans eseri olup olmadıgını kontrol edecegiz

#Gorev2:

#adım 1: hipotezleri tanımlayınız

#H0: M1=M2
#H1: M1!=M2

control_group["Purchase"].mean() #550

test_group["Purchase"].mean() # 582

#Normalllik varsayımı :
#H0: Normal dağılım varsayımı sağlanmaktadır.
#H1: Normal dağılım varsayımı sağlanmamaktadır
#p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

test_stat,pvalue = shapiro(control_group.Purchase)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat,pvalue)) #Reddediliemez

test_stat,pvalue = shapiro(test_group.Purchase)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat,pvalue)) #Reddedilemez normallik varsayımına uyuyor


#Varyans homojenligi
#H0: Varyanslarhomojendir
#H1: Varyanslarhomojen Değildir
#p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

test_stat,pvalue = levene(control_group.Purchase,
                          test_group.Purchase)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat,pvalue)) #Reddedilemez varyanslar homojen


test_stat,pvalue = ttest_ind(control_group.Purchase,
                             test_group.Purchase)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat,pvalue))
#Yani H0 hipotezini reddedemiyoruz. Yani her iki yöntem arasında anlamlı bir fark var diyemeyiz. H0: M1 = M2 reddedilemez.