

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 08:43:08 2021

@author: leaga
"""

import numpy as np
from tkinter import filedialog
from PIL import Image
import math
import os
import csv
import pandas as pd
import statistics
from read_roi import read_roi_zip
from shapely.geometry import Polygon


#########################
#
# Please specify which excel version you have
# (for German version ','; for English version '.')
#
#########################

comma_seperator = '.' 

#########################

#get the header of your file names to identify connected data
def fileNameGetter(s):
    name = s.split('.tif')
    new_name = name[0] + ".tif"
    new_name.rstrip()
    return new_name


#Open txt files (ROIs) with coordinates only of head
def readHeadRoi(path):

    #collected head_rois of one cell
    all_head_xy_data = []

    # Liste für die gesammelten xy-Daten von einem "head"-Abschnitt
    head_xy_data = []
    
    # Flag, um zu überprüfen, ob wir uns gerade im Abschnitt "head" befinden
    in_head_roi = False
    
    # Öffne die file im Lesemodus ('r' steht für "read")
    with open(path, 'r') as file:
        # Durchgehe jede row der file
        for row in file:
            # Überprüfe, ob die row "head" enthält
            if "head" in row:
                # Wenn wir bereits Daten für einen vorherigen "head"-Abschnitt gesammelt haben
                if head_xy_data:
                    # Füge die Daten zum Gesamtergebnis hinzu
                    all_head_xy_data.append(head_xy_data)
                    # Setze die Daten für den aktuellen "head"-Abschnitt zurück
                    head_xy_data = []
                # Setze das Flag für den "head"-Abschnitt
                in_head_roi = True
            elif "spine" in row or "neck" in row or "neck_skeleton" in row:
                # Setze das Flag zurück, wenn wir auf andere Abschnitte stoßen
                in_head_roi = False
            elif in_head_roi:
                # Sammle die xy-Daten, wenn wir uns im "head"-Abschnitt befinden
                xy_daten = [float(value) for value in row.split()]
                head_xy_data.append(xy_daten)

    # Füge die Daten des letzten "head"-Abschnitts hinzu, falls vorhanden
    if head_xy_data:
        all_head_xy_data.append(head_xy_data)
    
    """
    # Ausgabe der gesammelten "head"-Daten von allen Abschnitten
    for idx, head_daten in enumerate(all_head_xy_data):
        print(f"Head Daten für Abschnitt {idx + 1}: {head_daten}")
    """
    
    return all_head_xy_data

def readRoiPuncta(roi_zip_path):
    # Create a list to store the result
    roi_list = []
    
    #open the rois
    rois = read_roi_zip(roi_zip_path)

    for key, value in rois.items():
        xy_pairs = [[float(x), float(y)] for x, y in zip(value['x'], value['y'])]
        roi_list.append(xy_pairs)
        
    
    return roi_list

     
#calculates the given spine type
def spineType(path):
    spine_type_data = np.asarray(pd.read_csv(path, usecols=[1,2,7,8,11,12], names=['Length neck (micron)', 'Length spine (micron)', 'Perimeter Head (micron)', 'Area Head (micron²)', 'Average neckwidth (micron)','# Neckline'], header=None, decimal= comma_seperator, sep = '\t', encoding='latin1').replace(',', '.'))[1:]
    spine_type_list = []
    head_diameter_list = []
    count = 0
    
    filopodia_list = []
    stubby_list = []
    thin_list = []
    mushroom_list = []
    
    head_area_list = []
    filopodia_head_list = []
    stubby_head_list = []
    thin_head_list = []
    mushroom_head_list = []

    
    for nbrs in spine_type_data: 

        if nbrs[0] != nbrs[0]:
            continue
        else:
            nbrs[0] = float(nbrs[0].replace(',', '.'))
            nbrs[1] = float(nbrs[1].replace(',', '.'))
            nbrs[2] = float(nbrs[2].replace(',', '.'))
            nbrs[3] = float(nbrs[3].replace(',', '.'))
            nbrs[4] = float(nbrs[4].replace(',', '.'))
        #neck_length = nbrs[0]
        spine_length = nbrs[1]
        head_perimeter = nbrs[2]
        neck_diameter = nbrs[3]
        head_diameter = (head_perimeter/(math.pi))
        head_area = nbrs[4]
        #head_length = nbrs[1] - nbrs[0]
        print(spine_length)

        if spine_length > 2 or ((head_diameter/spine_length)<0.25 
                                and spine_length > 1.5):
            spine_type_list.append("filopodia")
            filopodia_list.append(head_diameter)
            filopodia_head_list.append(head_area)
        elif spine_length/head_diameter < 1.5 and spine_length < 1:
            spine_type_list.append("stubby")
            stubby_list.append(head_diameter)
            stubby_head_list.append(head_area)
        elif (head_diameter/neck_diameter > 1 and head_diameter > 0.6 
            and spine_length > 1):
            spine_type_list.append("mushroom")
            mushroom_list.append(head_diameter)
            mushroom_head_list.append(head_area)
        elif spine_length < 2:
            spine_type_list.append("thin")
            thin_list.append(head_diameter)
            thin_head_list.append(head_area)
        else:
            spine_type_list.append("unknown")
        head_diameter_list.append(head_diameter)
        head_area_list.append(head_area)
        count += 1

        
    return spine_type_list, head_diameter_list, filopodia_list, stubby_list, mushroom_list, thin_list, head_area_list, filopodia_head_list, stubby_head_list, mushroom_head_list, thin_head_list


#################### MAIN ####################


root_path = filedialog.askdirectory(title="Please select your folder with images to analyze")


#write the names of files down where errors occured
not_correct_spine = []


for condition_folder in os.listdir(root_path):
    
    if condition_folder.endswith(".tif"):
        example_image_path = os.path.join(root_path,condition_folder)
        continue
    
    #create dir for your condition results
    results_path_condition = os.path.join(root_path,"Analysis")
    if not os.path.exists(results_path_condition):
        os.makedirs(results_path_condition)
        
    if condition_folder == "Analysis":
        continue
    
    condition_path = os.path.join(root_path,condition_folder)
    print("Condition folder : ", condition_folder)
    
    
    
    #initialize your spine types
    spineTypes = {"filopodia", "stubby", "thin", "mushroom"}
    
    spine_data = {}
    
    
    #initialize analysis factors and set to zero for each condition --> summarized data  
    for spine_type in spineTypes:
        spine_data[spine_type] = {
            'file': [],
            'percentage': [],
            'total': [],
            'count': [],
            'PSD_0': [],
            'PSD_1': [],
            'PSD_SYN_0': [],
            'PSD_SYN_1': [],
            'diameter_PSD_0': [],
            'diameter_PSD_1': [],
            'diameter_PSD_SYN_0': [],
            'diameter_PSD_SYN_1': [],
            'head_PSD_0': [],
            'head_PSD_1': [],
            'head_PSD_SYN_0': [],
            'head_PSD_SYN_1': [],
        }


    for cells_folder in os.listdir(condition_path):
        
        if cells_folder == "Analysis":
            continue

        round_path = os.path.join(condition_path,cells_folder)
            
  
        print("Cells folder: ", cells_folder)

        
        for files in os.listdir(round_path):
            if files == "Analysis":
                continue
            
            if "spine.txt" not in files:
                continue
            
            #create dir for your cells results
            results_path_cell = os.path.join(round_path,"Analysis")
            if not os.path.exists(results_path_cell):
                os.makedirs(results_path_cell)
            
            #intialize temporary lists for storage of data to calculate intersections (should be emptied always inbetween)
            psd_list = []
            psd_roi_list = []
            syn_list = []
            syn_roi_list = []
            
            #get your files header to identify connected data
            file_header = fileNameGetter(files)
            print("file_header: ", file_header)

            csv_name = str(file_header + "_spine.xls")
            
            
            spine_data_cell = {}
            
            
            #initialize analysis factors and set to zero for each cell --> single data  
            for spine_type in spineTypes:
                spine_data_cell[spine_type] = {
                    'percentage': [],
                    'total': [],
                    'count': [],
                    'PSD_0': [],
                    'PSD_1': [],
                    'PSD_SYN_0': [],
                    'PSD_SYN_1': [],
                    'diameter_PSD_0': [],
                    'diameter_PSD_1': [],
                    'diameter_PSD_SYN_0': [],
                    'diameter_PSD_SYN_1': [],
                    'head_PSD_0': [],
                    'head_PSD_1': [],
                    'head_PSD_SYN_0': [],
                    'head_PSD_SYN_1': [],
                    
                }
                
            try: 
                csv_data = spineType(os.path.join(round_path,csv_name))
                spine_types = csv_data[0]
                #print("spine Types: ", spine_types)
                head_diameters = csv_data[1]
                head_areas = csv_data[6]
                
                filopodia_data = csv_data[2]
                stubby_data = csv_data[3]
                mushroom_data = csv_data[4]
                thin_data = csv_data[5]
                
                filopodia_head = csv_data[7]
                stubby_head = csv_data[8]
                mushroom_head = csv_data[9]
                thin_head = csv_data[10]
 
            except:
                print(f"Error: Analysis for {file_header} not possible. You probably have no {file_header}_spine.xls in your {cells_folder} folder.")
                continue
            
            spine_head_roi_name = str(file_header + "_spine.txt")
            head_rois = readHeadRoi(os.path.join(round_path, spine_head_roi_name))
            print("Head rois: ", len(head_rois))
            print("len spine types: ", len(spine_types))
            
            #check if everything is correct so far, length of spine_type and head_rois should be same, because nmbr of spines should be the same!
            if len(head_rois) != len(spine_types):
                print("Error: Your spine head roi data and spine type data do not have the same length. Somethihng is wrong with your data.")
                not_correct_spine.append(file_header)
                continue
            
            
            #load psd rois, structure: [[[x,y][x,y]],[[x,y][x,y]]]
            psd_roi_name = str(file_header + "PSD_ROI.zip")
            psd_rois = readRoiPuncta(os.path.join(round_path, psd_roi_name))
            
            #load syn rois, structure: [[[x,y][x,y]],[[x,y][x,y]]]
            syn_roi_name = str(file_header + "SYN_ROI.zip")
            syn_rois = readRoiPuncta(os.path.join(round_path, syn_roi_name))
            
            
            #go through all spines and check if there are intersections with syn and psd and check which spine type you have in
        
            
            for i, spine_type in enumerate(spine_types):
                head = head_rois[i]
                head_diameter = head_diameters[i]
                head_area = head_areas[i]
                
                #initialize variable to count intersections
                nmb_PSD_SYN = 0
                nmb_PSD = 0
                nmb_SYN = 0
                try: 
                    #create head polygon to try intersections
                    head_polygon = Polygon(head)
                    head_area = head_polygon.area
                    
                    for psd in psd_rois:
                        #do intersection spine head
                        psd_polygon = Polygon(psd)
                        psd_area = psd_polygon.area
    
                        intersection_area = psd_polygon.intersection(head_polygon).area
                        if (intersection_area != 0 and 
                            intersection_area/head_area < 0.5 and 
                            intersection_area/psd_area > 0.1):
                            nmb_PSD += 1
                            
                            #check for functional synapses
                            for syn in syn_rois:
                                 syn_polygon = Polygon(syn)
                                 syn_area = syn_polygon.area
                                 #intersection area for syn and psd
                                 intersection_area_PSDSYN = psd_polygon.intersection(syn_polygon).area
                                 if (intersection_area_PSDSYN != 0 and 
                                    intersection_area_PSDSYN/syn_area > 0.1 and 
                                    intersection_area_PSDSYN/psd_area > 0.1):
                                    nmb_PSD_SYN += 1
                                 
                    
                    #count PSDs
                    if nmb_PSD == 0:
                        spine_data_cell[spine_type]['PSD_0'].append(1)
                        spine_data_cell[spine_type]['diameter_PSD_0'].append(head_diameter)
                        spine_data_cell[spine_type]['head_PSD_0'].append(head_area)
                        
                    if nmb_PSD >= 1: 
                        spine_data_cell[spine_type]['PSD_1'].append(1)
                        spine_data_cell[spine_type]['diameter_PSD_1'].append(head_diameter)
                        spine_data_cell[spine_type]['head_PSD_1'].append(head_area)

                    #count number of functional synapses
                    if nmb_PSD_SYN == 0:
                        spine_data_cell[spine_type]['PSD_SYN_0'].append(1)
                        spine_data_cell[spine_type]['diameter_PSD_SYN_0'].append(head_diameter)
                        spine_data_cell[spine_type]['head_PSD_SYN_0'].append(head_area)
                    
                    if nmb_PSD_SYN >= 1:
                        spine_data_cell[spine_type]['PSD_SYN_1'].append(1)
                        spine_data_cell[spine_type]['diameter_PSD_SYN_1'].append(head_diameter)
                        spine_data_cell[spine_type]['head_PSD_SYN_1'].append(head_area)
                    

                        
                except:
                    print("Some of your ROI data are to small to process the intersections.")

        

            for spine in spineTypes:
                
                diameter_variable_name = f"{spine}_data"
                diameter_value = locals()[diameter_variable_name]  # Access variable dynamically
                spine_data_cell[spine]['count'].append(len(diameter_value))
                spine_data_cell[spine]['total'].append(len(spine_types))
                spine_data_cell[spine]["percentage"].append((len(diameter_value)/len(spine_types))*100)
                
                
                
                #fill the condition dictioanry
                spine_data[spine]['file'].append(file_header)
                
                spine_data[spine]['percentage'].append((len(diameter_value)/len(spine_types))*100)
                spine_data[spine]['total'].append(len(spine_types))
                spine_data[spine]['count'].append(len(diameter_value))
                
                spine_data[spine]['PSD_0'].append(len(spine_data_cell[spine]['PSD_0']))
                spine_data[spine]['PSD_1'].append(len(spine_data_cell[spine]['PSD_1']))
                spine_data[spine]['PSD_SYN_0'].append(len(spine_data_cell[spine]['PSD_SYN_0']))
                spine_data[spine]['PSD_SYN_1'].append(len(spine_data_cell[spine]['PSD_SYN_1']))
                
        
                try:
                    spine_data[spine]['diameter_PSD_0'].append(statistics.mean(spine_data_cell[spine]['diameter_PSD_0']))
                except:
                    spine_data[spine]['diameter_PSD_0'].append(pd.NA)
                try:
                    spine_data[spine]['diameter_PSD_1'].append(statistics.mean(spine_data_cell[spine]['diameter_PSD_1']))
                except:
                    spine_data[spine]['diameter_PSD_1'].append(pd.NA)
                try:
                    spine_data[spine]['diameter_PSD_SYN_0'].append(statistics.mean(spine_data_cell[spine]['diameter_PSD_SYN_0']))
                except:
                    spine_data[spine]['diameter_PSD_SYN_0'].append(pd.NA)
                try: 
                    spine_data[spine]['diameter_PSD_SYN_1'].append(statistics.mean(spine_data_cell[spine]['diameter_PSD_SYN_1']))
                except: 
                    spine_data[spine]['diameter_PSD_SYN_1'].append(pd.NA)
                    
                    
                try:
                    spine_data[spine]['head_PSD_0'].append(statistics.mean(spine_data_cell[spine]['head_PSD_0']))
                except:
                    spine_data[spine]['head_PSD_0'].append(pd.NA)
                try:
                    spine_data[spine]['head_PSD_1'].append(statistics.mean(spine_data_cell[spine]['head_PSD_1']))
                except:
                    spine_data[spine]['head_PSD_1'].append(pd.NA)
                try:
                    spine_data[spine]['head_PSD_SYN_0'].append(statistics.mean(spine_data_cell[spine]['head_PSD_SYN_0']))
                except:
                    spine_data[spine]['head_PSD_SYN_0'].append(pd.NA)
                try: 
                    spine_data[spine]['head_PSD_SYN_1'].append(statistics.mean(spine_data_cell[spine]['head_PSD_SYN_1']))
                except: 
                    spine_data[spine]['head_PSD_SYN_1'].append(pd.NA)
                
    
    
                # Find the maximum length of all values (lists) in the dictionary
                max_length = max(len(lst) for lst in spine_data_cell[spine].values())
                #print("max length: ", max_length)
                
                # Pad each list in the dictionary with NaN to ensure the same length
                for key in spine_data_cell[spine]:
                    current_length = len(spine_data_cell[spine][key])
                    if current_length < max_length:
                        spine_data_cell[spine][key] += [pd.NA] * (max_length - current_length)
                         
                #create a pandas dataframe of your dictionary
                df_single = pd.DataFrame(spine_data_cell[spine])
                
                #save .csv
                df_single.to_csv(results_path_cell + fr'/{spine}_{file_header}_single.csv', index=False)
            
            
            
            
        
            
    #write condition data to .csv --> summary of all data
    
    df_condition = pd.DataFrame(spine_data["filopodia"])
    df_condition.to_csv(results_path_condition + fr'/filopodia_{condition_folder}.csv', index=False)
    
    df_condition = pd.DataFrame(spine_data["stubby"])
    df_condition.to_csv(results_path_condition + fr'/stubby_{condition_folder}.csv', index=False)
    
    df_condition = pd.DataFrame(spine_data["thin"])
    df_condition.to_csv(results_path_condition + fr'/thin_{condition_folder}.csv', index=False)
    
    df_condition = pd.DataFrame(spine_data["mushroom"])
    df_condition.to_csv(results_path_condition + fr'/mushroom_{condition_folder}.csv', index=False)
    

#print out all the cells where error occured

df = pd.DataFrame(not_correct_spine, columns = ["Errors"])
df.to_csv(results_path_condition + r'/Errors_in_Cells.csv', index=False)

            


  
            
            
            
   





    
    
    

 