##################################################################
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
import statsmodels.stats.proportion as proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

##################  Görev 1: Veriyi Hazırlama ve Analiz Etme #####################
## Adım 1: ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız

control = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
test = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

## Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control.describe().T
test.describe().T

## Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df = pd.concat([control, test], axis=0, ignore_index=True )
df.head()

##################### Görev 2: A/B Testinin Hipotezinin Tanımlanması ##################

##Adım 1: Hipotezi tanımlayınız.

# H0 : M1 = M2  iki grup ortalaması arasında anlamlı bir farklılık yoktur
# H1 : M1!= M2  iki grup ortalaması arasında anlamlı bir farklılık vardır

## Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.

control["Purchase"].mean()
test["Purchase"].mean()

######################## Görev 3: Hipotez Testinin Gerçekleştirilmesi   ###########################

#Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.

#Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

##### Normallik Varsayımı  ##############

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ? Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = shapiro(test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

                                # p-value=0.1541 > 0.05 do not reject
                                # Normallik varsayımı sağlanmaktadır

test_stat, pvalue = shapiro(control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

                                # p-value=0.5891 > 0.05 do not rej
                                # Normallik varsayımı sağlanmaktadır


#### Varyans Homojenliği ##############

# H0: Varyanslar homojendir.
# H1: Varyanslar homojen değildir.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
# Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını Purchase değişkeni üzerinden test ediniz.
# Test sonucuna göre normallik varsayımı sağlanıyor mu? Elde edilen p-value değerlerini yorumlayınız.

test_stat, pvalue = levene(test["Purchase"],
                           control["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))             # p-value=0.1083 > 0.05
                                                                             # Varyanslar homojendir
    
    
################################  Görev 4: Sonuçların Analizi  ########################################

#Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

#Ortalamalar kıyaslandığından normallik varsayımı sağlanıyorsa parametrik (T test), sağlanmıyorsa non-parametrik (mannwhitneyu) test kullanmalıyız
#Varsayımlar sağlandığı için parametrik test olan T test i kullandık

#Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

# Test sonuçlarına göre "maximumbidding" adı verilen teklif verme türü ile "average bidding" 'in getirdiği oralamat kazançlar arasında istatistiki 
# olarak anlamlı bir farklılık yoktur.
# Bu durumda teklif verme sisteminde geliştirme yapılmadığı sürece average bidding uygulaması anlamlı bir fark yaratmayacaktır.
# Bir süre daha gözlem yapılarak ve veri sayısı arttırılarak daha büyük bir örneklem kütlesi ile aynı testler tekrarlanabilir.
