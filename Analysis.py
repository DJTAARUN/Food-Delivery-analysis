import pandas as pd 
import matplotlib.pyplot as plt 
from collections import Counter as ct
 
df = pd.read_csv("food delivery costs.csv")

#To check the top 5 rows
df.head()

#To provide information about th data
df.info()

#Cleaning the column to correct data type
df["Order Date and Time"] = pd.to_datetime(df["Order Date and Time"])
df["Delivery Date and Time"] = pd.to_datetime(df["Delivery Date and Time"])

#Standardising discounts and offers column by extracting the percent value
def to_extract(value):
  a = str(value).split(" ")
  return a[0]

df["Discounts and Offers"] = df["Discounts and Offers"].apply(to_extract)

#To remove percent value in discounts
def removep(value):
  if "%" in value:
    b = value.replace("%","")
    return float(b)
  else:
    return float(value)

df["Discounts and Offers"] = df["Discounts and Offers"].apply(removep)

#Converting percent value into rupees
df.loc[(df["Discounts and Offers"] <= 15),"Discounts and Offers"] = (df["Discounts and Offers"]/100)* df["Order Value"]

#Converting none valies to zero
df["Discounts and Offers"] = df["Discounts and Offers"].fillna(0)

#Calculating profit of the app with comission fee analysis
df["Costs"] = df["Delivery Fee"] + df["Discounts and Offers"] + df["Payment Processing Fee"]
df["Profit"] = df["Commission Fee"] - df["Costs"]
c=df["Profit"].sum()

#To check distribution of fees
cost_dist = df[["Delivery Fee", "Payment Processing Fee", "Discounts and Offers"]].sum()
cost_dist
#to show payment methods used
ps = df["Payment Method"].str.cat(sep=", ")
pl = ps.split(", ")
pc = ct(pl)
labels = list(pc.keys())
sizes = list(pc.values())
#To show in charts or other distribution of the columns
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
fig.tight_layout(pad=5.0)

axs[0,0].pie(cost_dist, labels = cost_dist.index, autopct = "%1.2f%%")

abc=df[["Commission Fee", "Costs", "Profit"]].sum()

axs[0,1].bar(abc.index, abc)

axs[1,0].hist(df["Profit"])

axs[1,1].pie(sizes, labels=labels, autopct="%1.1f%%")

fig.tight_layout(pad=5.0)


df.head()
plt.show()