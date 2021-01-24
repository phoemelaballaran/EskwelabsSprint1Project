import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


#-----Start of Set Up-----#

my_page = st.sidebar.radio('Contents',['Introduction','Data Information','Methodology', 'EDA','Cluster Analysis','Other Cluster Insights','Conclusions and Recommendations']) # creates sidebar #

st.markdown("""<style>.css-1aumxhk {background-color: #ebeae3;background-image: none;color: #ebeae3}</style>""", unsafe_allow_html=True) # changes background color of sidebar #

#-----End of Set Up-----#


#-----Start of Page 1 (Introduction)-----#

if my_page == 'Introduction':

    st.title("Allocation of Resources for School Congestion in Elementary Schools")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between title and paragraph #
    st.markdown("To achieve accessible, relevant, and liberating basic education for all, the Philippine Development Plan 2017-2022 identifies the following as part of the country’s core strategies: (1) Increasing investments  in education to improve quality, and (2) Extending opportunities to those outside of the formal education.")
    c1, c2 = st.beta_columns(2)
    c1.markdown('<div style="text-align: center;color: #F7A92D; font-size: large;font-weight: bold;">Increasing Investments</div>',unsafe_allow_html=True)
    c1.image('increasinginvestments.png',use_column_width=True)
    c2.markdown('<div style="text-align: center;color: #A6C3D0; font-size: large;font-weight: bold;">Extending Opportunities</div>',unsafe_allow_html=True)
    c2.image('extendingopportunities.png',use_column_width=True)
    st.markdown("As part of the strategy of increasing investments in education, we wanted to know how the Department of Education can target their efforts and resources to address congestion in elementary schools.")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between paragraph and image #
    st.image('overpop.png',use_column_width=True)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between paragraph and image #
    st.markdown("But school congestion is a nuanced and complex concept, which cannot be capture by a single indicator alone. So we used three indicators such as the (1) student-teacher ratio, (2) student per school room ratio, and (3) MOOE per student. Using these indicators as features, we performed a clustering algorithm on our data to come up with clusters, which then could help the Department of Education in focusing their resources on clusters that may be in need of those resources more.")
    
    
#-----End of Page 1 (Introduction)-----#


#-----Start of Page 2 (Data Information)-----#

elif my_page == 'Data Information':
    
    st.title("Data Information")
    st.image('datainfo1.png',use_column_width=True)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between image and paragraph #
    st.markdown("We used public data from the Department of Education dated 2015. The seven datasets we used provided information on the masterlist of schools and their number of teachers, Maintenance and Other Operating Expenses (MOOE),  rooms, location, and enrollees, as well as enrollee information like gender, grade level, and class type (regular and SPED).")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between image and paragraph #
    st.image('datainfo2.png',use_column_width=True)
    st.markdown("After merging the different datasets into one master data, we processed it to obtain only the elementary school data, as well as created the different ratios we will be needing for the modelling. 14.73% or 5,282 rows were removed from the elementary school data when the outliers were filtered out.")
    
#-----End of Page 2 (Data Information)-----#


#-----Start of Page 3 (Methodology)-----#

elif my_page == 'Methodology':
    st.title("Methodology")
    st.image('methodology.png',use_column_width=True)
    st.markdown("We created a master data where we merged all of the seven source data. We then proceeded to drop the zero and missing values, and filtered the dataset to elementary.")
    st.markdown("From there, we engineered three features that we deemed helpful in answering our problem (such as the student-teacher ratio, student per school room ratio, and MOOE per student ratio). We proceeded to prepare the data for the modelling by dropping the outliers so that they won’t skew the clustering. After dropping the outliers, the dataset is scaled and then fed to different models.")
    st.markdown("We tested both Hierarchical and KMeans modelling and settled on using KMeans with 3 clusters based on the model’s silhouette score and the amount of distribution among the clusters.")

#-----End of Page 3 (Methodology)-----#


#-----Start of Page 4 (EDA)-----#

elif my_page == 'EDA':
    st.title("Exploratory Data Analysis")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between subheader and graph #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between subheader and graph #
    st.subheader("Student-Teacher Ratio")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between subheader and graph #
    
    # start of data prep for maps #
    shapefile = gpd.read_file('map_data_clean.shp')
    df_st_ratio = pd.read_csv('df_st_ratio.csv')
    merged_data = pd.merge(shapefile, df_st_ratio, left_on='PROVINCE', right_on="school.province")
    # end of data prep for maps #
    
    # start of generating map for student/teacher ratio #
    c1, c2 = st.beta_columns(2)
    variable = "student_teacher_ratio"

    vmin, vmax = merged_data["student_teacher_ratio"].min(), merged_data["student_teacher_ratio"].max()

    fig, ax = plt.subplots(1, figsize=(15, 10))

    cmap = mpl.cm.Oranges(np.linspace(-0.5,1,23))
    cmap = mcolors.ListedColormap(cmap[10:,:-1])

    merged_data.plot(column=variable, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
    ax.grid(False)
    plt.title("Average Student-Teacher Ratio Per Province",fontsize=18,y=1.02)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)

    # end of generating map for student/teacher ratio #
    
    c1.pyplot(fig) # show graph #
    
    # start of insights #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between graph and insights #
    st.markdown('Provinces like Rizal, Bulacan, and Cebu have the highest average student-teacher ratio; while most of the regions in Luzon like CAR, Region I and II enjoys the lowest average student-teacher ratio.')
    # end of insights #
    
    # start of generating map for student per room ratio #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between subheader and graph #
    st.subheader("Student Per Room Ratio")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between subheader and graph #
    c3, c4 = st.beta_columns(2)
    variable = "student_per_rm"

    vmin, vmax = merged_data["student_per_rm"].min(), merged_data["student_per_rm"].max()

    fig, ax = plt.subplots(1, figsize=(15, 10))

    cmap = mpl.cm.Oranges(np.linspace(-0.5,1,23))
    cmap = mcolors.ListedColormap(cmap[10:,:-1])

    merged_data.plot(column=variable, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
    ax.grid(False)
    plt.title("Average Student Per Room Ratio Per Province",fontsize=18,y=1.02)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)

    # end of generating map for student per room ratio #
    
    c3.pyplot(fig) # show graph #
    
    # start of insights #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between graph and insights #
    st.markdown('High student-room ratio in NCR, South Luzon, and Mindanao; lower student-room ratio in North Luzon.')
    # end of insights #
    
    # start of generating map for mooe per student ratio #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between subheader and graph #
    st.subheader("MOOE Per Student Ratio")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between subheader and graph #
    c5, c6 = st.beta_columns(2)
    variable = "student_per_rm"

    vmin, vmax = merged_data["student_per_rm"].min(), merged_data["student_per_rm"].max()

    fig, ax = plt.subplots(1, figsize=(15, 10))

    cmap = mpl.cm.Oranges(np.linspace(-0.5,1,23))
    cmap = mcolors.ListedColormap(cmap[10:,:-1])

    merged_data.plot(column=variable, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
    ax.grid(False)
    plt.title("Average Student Per Room Ratio Per Province",fontsize=18,y=1.02)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)

    # end of generating map for mooe per student ratio #
    
    c5.pyplot(fig) # show graph #
    
    # start of insights #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between graph and insights #
    st.markdown('High MOOE per student in Northern Luzon, Samar, Zamboanga; low MOOE per student in Southern Luzon, and the regions around Cotabato.')
    # end of insights #
    
#-----End of Page 4 (EDA)-----#


#-----Start of Page 5 (Cluster Analysis)-----#

elif my_page == 'Cluster Analysis':
    
    st.title("Cluster Analysis")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space subheader and graph #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space subheader and graph #
    
    st.image('spider_clusters.png',use_column_width=True)
    
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between graph and insights #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between graph and insights #
    st.markdown('<div style="font-size: medium;padding-bottom: 15px;font-weight:bold">Cluster 1: Schools with low demand & high resources</div>',unsafe_allow_html=True)
    st.markdown('• Mostly situated in rural areas')
    st.markdown('• Low student-teacher ratio')
    st.markdown('• Low student per room ratio')
    st.markdown('• High MOOE per student')
    
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between graph and insights #
    st.markdown('<div style="font-size: medium;padding-bottom: 15px;font-weight:bold">Cluster 2: Schools with high demand & low resources</div>',unsafe_allow_html=True)
    st.markdown('• Mostly situated in urban areas')
    st.markdown('• High student-teacher ratio')
    st.markdown('• High student per room ratio')
    st.markdown('• Low MOOE per student')
    
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between graph and insights #
    st.markdown('<div style="font-size: medium;padding-bottom: 15px;font-weight:bold">Cluster 3: Schools with moderate demand & resources</div>',unsafe_allow_html=True)
    st.markdown('• Found in both urban/rural areas')
    st.markdown('• Moderate student-teacher ratio')
    st.markdown('• Moderate student per room ratio')
    st.markdown('• Moderate MOOE per student')
    
    # mapping clusters #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    st.subheader("Mapping schools belonging to the different clusters")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    from shapely.geometry import Point, Polygon
    df_map = pd.read_csv('mappingclusters.csv')
    shapefile = gpd.read_file('map_data_clean.shp')
    geometry = [Point(xy) for xy in zip(df_map['Longitude'], df_map['Latitude'])]
    geo_df = gpd.GeoDataFrame(df_map, geometry = geometry)
    c1, c2 = st.beta_columns(2)
    option = c2.selectbox('Which cluster do you want to see?', [1, 2, 3])
    
    if option == 1:
        color = "#A6C3D0"
        c2.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
        c2.markdown('Cluster 1 is abundant in upper Luzon (e.g. Isabela, Iloilo, Pangasinan), Western & Eastern Visayas (e.g. Leyte, Bohol). It is least common in NCR.')
    elif option == 2:
        color = "#BD4C2F"
        c2.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
        c2.markdown('Cluster 1 is abundant in upper Luzon (e.g. Isabela, Iloilo, Pangasinan), Western & Eastern Visayas (e.g. Leyte, Bohol).')
    else:
        color = "#FccF55"
        c2.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
        c2.markdown('Cluster 3 is abundant in upper Luzon (e.g. Pangasinan, Iloilo, Isabela), Western & Eastern Visayas (e.g. Leyte, Negros Occidental).')
        
    fig, ax = plt.subplots(figsize=(15, 15))
    shapefile.plot(ax=ax, alpha = 0.4, color='grey')
    geo_df[geo_df['clusters']==(option-1)].plot(ax=ax, marker='+',color=color, markersize=8)
    plt.title("Map of Schools in Cluster " + str(option) ,fontsize=22,y=1.02)
    
    # end of generating map #
    
    c1.pyplot(fig) # show graph #
#-----End of Page 5 (Cluster Analysis)-----#


#-----Start of Page 6 (Other Cluster Insights)-----#

elif my_page == 'Other Cluster Insights':

    st.subheader("Majority of Elementary Schools in the Philippines are managed by DepEd and are in a monograde setup")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    df_mgmt = pd.read_csv('df_mgmt.csv')    
    df_mgmt = df_mgmt.rename(columns={'school.classification2' : 'Management Classification'})
    mycolors = ["#A6C3D0","#BD4C2F","#FccF55"]
    sns.set_palette(sns.color_palette(mycolors))
    sns.set_style("whitegrid")
    fig=plt.figure(figsize=(9,7))
    sns.barplot(x='clusters', y='total_count', hue='Management Classification', data=df_mgmt)
    plt.xlabel('Clusters',fontsize=12)
    plt.ylabel("Number of Schools",fontsize=12)
    plt.xticks(ticks = (0, 1, 2), labels = ['1', '2', '3'])
    plt.title("School Management Classification per Cluster",fontsize=15,y=1.02)
    st.pyplot(fig)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    df_org = pd.read_csv('df_org.csv')    
    df_org = df_org.rename(columns={'school.organization' : 'Organization Type'})
    mycolors = ["#A6C3D0","#BD4C2F","#FccF55"]
    sns.set_palette(sns.color_palette(mycolors))
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(9,7))
    sns.barplot(x='clusters', y='count', hue='Organization Type', data=df_org)
    plt.xlabel('Clusters',fontsize=12)
    plt.ylabel("Number of Schools",fontsize=12)
    plt.xticks(ticks = (0, 1, 2), labels = ['1', '2', '3'])
    plt.title("School Organization per Cluster",fontsize=15,y=1.02)
    st.pyplot(fig)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    st.subheader("SPED opportunities are present in clusters where schools are mostly in urban locations")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True)
    spedcount = pd.read_csv('spedcount.csv') 
    fig=plt.figure(figsize=(9,7))
    sns.barplot(x="clusters", y='total_enrollees_sped', data=spedcount)
    plt.xlabel('Clusters',fontsize=12)
    plt.ylabel("SPED Enrollees",fontsize=12)
    plt.xticks(ticks = (0, 1, 2), labels = ['1', '2', '3'])
    plt.title("Incidence of SPED Enrollees per Cluster",fontsize=15,y=1.02)
    st.pyplot(fig)

#-----End of Page 6 (Other Cluster Insights)-----#


#-----Start of Page 7 (Conclusions and Recommendations)-----#

elif my_page == 'Conclusions and Recommendations':

    st.title("Conclusions and Recommendations")
    st.image('conclusion.jpg',use_column_width=True)
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between subheader and paragraph #
    st.subheader("Regarding the Philippine Education Based on the Data Insights")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between title and subheader #
    st.markdown(':bulb:  Consider giving more resources to urban areas given their higher school congestion')
    st.markdown(':bulb:  Examine reasons for low congestion in rural areas')
    st.markdown('  - Look into other factors that affect access to schools (e.g. transportation, economic situation of families, etc) that may prevent students from going to schools - that may lead to underutilization of  resources')
    st.markdown(':bulb:  Address the low incedence of SPED enrollees in rural areas')
    st.markdown('  - For areas which do not have SPED offerings, where do students who need SPED go to?')
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between title and subheader #
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between title and subheader #
    st.subheader("Regarding the Machine Learning Aspect")
    st.markdown('<div style="color: #FFFFFF;">.</div>',unsafe_allow_html=True) # for space between title and subheader #
    st.markdown(':bulb:  Look into other features which may better categorize schools and improve clustering statistics like the inertia score and silhouette score.')
    st.markdown(':bulb:  Experiment with the different hyperparameters for K-Means and Hierarchical Clustering (init, distance metrics, linkages). Also check if there are other algorithms that may result to better clustering.')

#-----End of Page 7 (Conclusion and Recommendation)-----#