### Melbourne
Since the 1980s Melbourne has been actively pursuing an agenda to improve public life in the city centre. In the preceding period, the central business distict had been declining as it lost both residents and retail to suburban areas more accessible by car. Part of the efforts to revitalise the city centre has included the Places for People study. The initial study was published in 1994 and surveyed the types of activities occuring in the city's public spaces as well as making ten year targets for increasing footfall in the city centre. Subsequent studies in 2004 and 2014 have allowed longer term study of how (and why) the city's urban environment is changing. 

The results do show that the city has undergone substantial (positive) changes, with substantial growth in footfall and a return of both businesses and residences to the city centre. The 2015 Places for People study notes that growth in footfall isn't uniform across the city. Whilst it has been rising in the city centre, this hasn't been the case in other parts of the city. The Docklands and South Bank are areas which have experienced high density growth in retail and accommodation, but footfall hasn’t grown concurrently as we might perhaps expect.

The Places for People research defines four categories of influence on footfall:<sup>3</sup>
* Land uses (Land uses are those activities that occur inside buildings)
* Urban form (spatial arrangement of a city’s primary organising components: the street blocks, street network, land parcels, and natural physical features)
* Public space (communal social space that is accessible to all people: including Streets and malls, laneways; urban squares and plazas; parks and gardens; river ways and promenades. 
* Movement (how navigatable the city is, especially walkability)
* Built form (physical shape and scale of buildings (height, width,depth) and bulding architectural details)

The 2015 report suggests that the highest footfall counts are on streets with pedestrian friendly design, and with proximity to public transport nodes and high land use intensity (e.g. lots of different land uses). 

Other things mentioned in detail:
* The importance of the restoration of laneways is also emphasised. These narrow alleys/streets are described as having become neglected and were being increasingly used solely for rubbish collection, with just 8% accessible in 1994. However, by 2004 92% had become walkable and often featured new cafes and restaurants.<sup>1</sup>
* Towers (defined as buildings over 18 storeys). They demonstrate that towers, and podium towers in particular, lead to a poorer interface between the building and the public environment (diminishing people's sense of connectedness to the street).
* Building entrances - this is mentioned as a determinant of footfall as more building entrances means more land uses to access.
* Population 
* Number of jobs 
* Disparity between foot traffic in the day and at night, and notes that the evening closure of arcades both affects the feel of the areas surrounding them and decreases the permeability of the pedestrian network. 

## General research into influences on footfall

Footfall is clearly determined by numerous factors on different spatial and temporal scales; however, there has been limited research which has quantified the links between footfall and these factors. Research by Philp et al (2022)<sup>3</sup> does attempt to do this and lists the main determinants of footfall as being:
* Physical characteristics (density of retail units, presence of anchor stores, workplace population)
* Security
* Network connectivity - how the street is situated within a wider network has proven to be a reliable indicator of pedestrian counts (Hillier et al., 1993; Raford & Ragland, 2006). Well-connected streets which provide lots of people with the shortest route from their origin to destination tend to have higher footfall. This can be measured by closeness and betweenness. 
* Transport connectivity (in particular, walkability, the attractiveness of streets to pedestrians and their accessibility to other forms of transport)

This research specifically uses a range of variables to classify the location of footfall sensors on the basis of their surroundings (chain and comparison retail micro-locations, business and independent micro-locations and value-orientated convenience retail micro-locations). The variables they use in this classification are:
 
|Category|Variable|Specification|
|---|---|---|
| Functionality | Distance to the nearest anchor store | Euclidean distance (metres) to nearest anchor store, identified by their brand name (e.g. John Lewis, Primark, Debenhams, full list in Appendix C) |
|  | Distance to the nearest premium store | Euclidean distance (metres) to the nearest premium store, identified by their brand names (e.g. The White Company, Burberry, full list in Appendix C) |
|  | Distance to the nearest entertainment activity | Euclidean distance (metres) to the nearest venue which offers an entertainment activity (e.g. Cinemas, Arcades, Museums). These were identified using the LDC (2017) survey sub-categorisation (full specification in Appendix C) |
|  | Proportion of vacant stores (vacancy rate) | The proportion of vacant store identified using the LDC (2017) survey within a 100 m straight line buffer of the sensor |
|  | Proportion of value stores | The proportion of stores identified as value stores by their brand name (e.g. Aldi, Home Bargains, full list in Appendix C) within a 100 m straight line buffer of the sensor |
|  | Proportion of independent stores | The proportion of stores identified as independent by the singular instance of their store name in the dataset within a 100 m straight line buffer of the sensor |
|  | Proportion of night-time economy locations | The proportion of locations within a 100 m straight line buffer of the sensors which offer a typical evening appeal (e.g. bars, clubs, restaurants, fast food) identified using LDC (2017) survey categorisation (full specification in Appendix C) |
|  | Workplace population | The average of the daytime population densities of the workplace zone in which the sensor falls into, and those which border it (ONS, 2017) |
|  | Ratio of service to retail | The ratio of the locations within a 100 m straight line buffer of the sensor which are identified as service locations by LDC (2017) survey classifications to those identified as comparison retail and food retail (e.g. grocery stores, butchers, confectioners, further specifics in Appendix A) |
| Morphology and Connectivity | Distance to the nearest transport hub | Euclidean distance (metres) to the nearest group of bus stops or train station as identified in the NaPTAN dataset (Department for Transport, 2014) |
|  | Distance to the nearest car park | Euclidean distance (metres) to the nearest car park as identified by the Department for Transport (2015) |
|  | Density of stores | The number of store units within a 100 m straight line buffer of the sensor |
|  | Centrality of the street | The street centrality measure was calculated from networks generated by the OSMnx python library. OSMnx uses data from Open Street Map to generate a network graph of a road structure within a boundary. The CDRC retail centre boundaries (Pavlis et al., 2017) were used to generate the pedestrian network around a sensor. The edge betweenness centrality of the street which the sensor was on was is then calculated to give the street centrality measure. Edge betweenness was chosen as the centrality measure because it can be applied to streets instead of intersections, where most of the footfall measurements are taken from. This captures the prominence of a street as a pass-through route |


Analyses differences in footfall before and after the clocks change, and also how the provision of lighting affects this.<sup>5</sup>
### References
<sup>1</sup> https://www.livingstreets.org.uk/media/3890/pedestrian-pound-2018.pdf)
<sup>2</sup>https://www.melbourne.vic.gov.au/building-and-development/urban-planning/city-wide-strategies-research/Pages/places-for-people.aspx  
<sup>3</sup>https://www.melbourne.vic.gov.au/SiteCollectionDocuments/places-for-people-2015.pdf
<sup>4</sup>https://link.springer.com/article/10.1007/s12061-021-09396-1 -- Archetypes of Footfall Context: Quantifying Temporal Variations in Retail Footfall in relation to Micro-Location Characteristics 
<sup>5</sup>Does lighting affect pedestrian flows? A pilot study in Lund, Market Harborough and Dublin.  
