# SpineMorphology
Analyze spine types and functional synapses with imaging data. For this, you need cells stained for pre-and postsynapses as well as neurons (so that you spines are visible). Analyses of only spine types without functional synpases is possible. 
Data obtained with the SpineJ plugin are used for morphological features of dendritic spines (Levet et al., 2020). To access the neck and head coordinates, the source code of SpineJ was adapted in the NeuronDisplayDialog class, see details [here](https://github.com/LeaMyCode/SpineJ_changes). The altered .jar can be found above.

Additionally, a code using manual obtained spine features (measuring width of neck and heads in FIJI) can be found [here](https://github.com/LeaMyCode/ManualSpineTypes-GOLGI-).


## Example of spine types and functional synapses
![image](https://github.com/user-attachments/assets/1b83bec0-b093-4818-a7ac-cc8383578037)

_(A) Example image of dendritic spines labelled with m-citrine (blue) and immunostaining of synaptophysin (green) and PSD95 (red). The white arrows show spines with postsynaptic density and the yellow arrow shows a functional spine, indicated by overlapping synaptophysin and PSD95 puncta within the respective spine head. Scale bar: 1 µm. (B) Example image of the same dendritic spines with marked spine types. Spines are divided into filopodia, stubby, thin and mushroom spines are the needed characteristics to belong to each spine type is listed._

## Please cite the following if you use the code
### SpineJ 
> Levet, F., Tønnesen, J., Nägerl, U. V., and Sibarita, J. B. (2020). SpineJ: A software tool for quantitative analysis of nanoscale spine morphology. Methods 174, 49–55. doi: 10.1016/j.ymeth.2020.01.020
### Spine type and functional synapse classification
> Gabele, L., Bochow, I., Rieke, N., Sieben, C., Michaelsen-Preusse, K., Hosseini, S., et al. (2024). H7N7 viral infection elicits pronounced, sex-specific neuroinflammatory responses in vitro. Front Cell Neurosci 18. doi: 10.3389/fncel.2024.1444876
