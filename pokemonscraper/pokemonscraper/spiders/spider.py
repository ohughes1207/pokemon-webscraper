# -*- coding: utf-8 -*-
"""
Created on Tue May 23 02:59:49 2023

@author: Olliver
"""

'''
TODO: Fix null generation for paradox pokemon

This can be done by changing method for scraping method to accessing the p element and scraping the text that follows "introduced in"

###################### DONE ##################

############# THIS HAS BEEN IMPLEMENTED AND BELIEVED TO BE WORKING AS EXPECTED#########

TODO: Make scraping groups functional

For legendary, Mythical and Paradox pokemon we can access the same p element used to fix null generation and check for 'Legendary' and 'Paradox' in the text with if statements

For Ultrabeasts we can access the p element that describes the pokemon as a Ultra beast and use if statement to append "Ultra Beast" to the list of groups the Pokemon is in

For Mega variants we can use an if statement to append 'Mega' to the list of groups if Mega is in the name of the pokemon

############ THIS HAS BEEN IMPLEMENTED AND BELIEVED TO BE WORKING AS EXPECTED ########

TODO: Make type scraping work for Mega variants and alternate formes

no clue how I'm going to approach this



TODO: Come up with method to remove 'Unknowns' if type list length exceeds the variant list length

################ Done ##############


TODO: Fix outliers

Darmanitan
Pikachu
Pumpkaboo
Gourgeist

######## This will be done through a Jupyter notebook while cleaning and preparing the data #######


TODO: make method to add variant names to Zacian and Zamazenta


####### Done #######


'''


import scrapy
from scrapy import Request

#Used to check if any string in the checklist paramater (a list of strings to check for) is in any element of a given list
def IsRegional(alist, checklist):
    for x in alist:
        if any(a in x for a in checklist):
            return True
        else:
            pass
    return False


class PokemonSpider(scrapy.Spider):
    name = 'pokemonscraper'
    start_urls = ['https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number']
    '''
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy.pipelines.images.ImagesPipeline': 1
        },
        'IMAGES_STORE': './img/'
    }
    '''
    def parse(self, response):
        #Extracts the paths of all tables with the table.roundy selector into a list
        tables = response.css('table.roundy')
        
        #loop through the the list of tables to get all pokemon in each table
        for table in tables:
            #Get the elements for all pokemon inside the table (skip the first element to ignore the labels in the tables)
            all_pkm = table.xpath('tbody/tr')[1:]
            #Loop through the list for all pokemon
            for pkm in all_pkm:
                #Get the Pokedex Number for the pokemon
                dex_n = pkm.xpath('td[1]//text()').get()
                #Alternate forms and Regional forms do not have a pokedex number in their element path and those with a pokedex number of #0000 are leaked pokemon so we can ignore them
                #We will get the Alternate and regional forms when getting data for the primary pokemon
                if dex_n is not None and dex_n!='#0000':
                    print(dex_n)
                    #href link to get to the primary pokemons main page
                    pkm_link=pkm.xpath('td[3]/a/@href').get()
                    #follow the link and use the get_pkms function to get the data
                    yield response.follow(pkm_link, callback= self.get_pkms)
                else:
                    continue
                
    #
    def get_pkms(self, response):
        #Get the generation the pokemon was introduced in
        gen= [x for x in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall() if 'Generation' in x][0]
        #Get the Pokedex number again as the previous pokedex number was just to check if the iteration was a regional form or a leaked pokemon
        dex_n = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/th/big/big/a/span/text()').get()
        #The name of the primary pokemon
        pkm_name = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/big/big/b/text()').get()
        #When a pokemon has multiple forms they can have a different combination of types so we can get their types into a list to loop through
        t1_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[1]/a/span/b/text()').getall()
        t2_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a/span/b/text()').getall()
        
        #Get all existing variant of the pokemon (including the primary form of the pokemon, only gets primary form of the pokemon also if alternate variants exist)
        variant_list = [x for x in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/small/text()').getall() if 'Gigantamax' not in x]# if pkm_name in x] #and 'Gigantamax' not in x]
        
        #If there are no alternate form of the pokemon then length of the variant_list is 0 so we can reassign it like so
        if len(variant_list)==0:
            variant_list=[pkm_name]
        
        #Extract all stats of the pokemon into a list that can be found on the page
        hp_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[3]/th/div[2]/text()').getall()
        att_list =  response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[4]/th/div[2]/text()').getall()
        def_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[5]/th/div[2]/text()').getall()
        sp_att_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[6]/th/div[2]/text()').getall()
        sp_def_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[7]/th/div[2]/text()').getall()
        speed_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[8]/th/div[2]/text()').getall()
        img_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/a[@class="image"]/@href').getall()
        
        #Lists containing keywords for regional and alternate forms that may appear in the names of Pokemon
        regional_forms = ['Paldean', 'Hisuian', 'Galarian', 'Alolan']
        alt_forms = [' Form', ' Mode', ' Build', 'Crowned', 'Hero ', ' Style', 'Family ', 'Normal', 'Size', 'Plumage', 'Breed', 'Cloak']
        
        #Extract the total stats for all the pokemon
        total_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[9]/th/div[2]/text()').getall()
        
        while len(img_list) < len(set(variant_list)):
            img_list=img_list.append(img_list[-1])


        print(variant_list)
                    
        
        
        #Truncate list of types incase they are longer than the list of variants
        if len(t1_list) > len(variant_list):
            t1_list=t1_list[0:len(variant_list)]
        if len(t2_list) > len(variant_list):
            t2_list=t2_list[0:len(variant_list)]
        

        if len(t1_list)==len(variant_list):
            
            
            #Outliers in this if statement are Darmanitan and Pikachu
            if len(total_list) < len(variant_list):
                for i in range(1, len(variant_list)):
                    
                    
                    hp_list=hp_list+hp_list
                    att_list=att_list+att_list
                    def_list=def_list+def_list
                    sp_att_list=sp_att_list+sp_att_list
                    sp_def_list=sp_def_list+sp_def_list
                    speed_list=speed_list+speed_list
                    total_list=total_list+total_list
                    
                    #len(set()) checks for how many unique values there are in the list
                    if len(set(hp_list))==1 and len(set(att_list))==1 and len(set(def_list))==1 and len(set(sp_att_list))==1 and len(set(sp_def_list))==1 and len(set(speed_list))==1 and len(set(total_list))==1:
                        print(t1_list)
                        print(t2_list)
                
                        if (len(set(t1_list))==2 and len(set(t2_list))==2 and IsRegional(variant_list, regional_forms)==False) or (len(set(t1_list))==2 and len(set(t2_list))==1 and IsRegional(variant_list, regional_forms)==False):
                            variant_list=[pkm_name]
                        
                    variant_list= sorted(set([x.replace('(', '').replace(')', '') for x in variant_list]), key=[x.replace('(', '').replace(')', '') for x in variant_list].index)
                        
            
            elif len(total_list)//len(variant_list)==2:
                
                if len(set(variant_list))>=2 and any('Generation' in s for s in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/h4/span/text()').getall()) and any(' onward' in s for s in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/h4/span/text()').getall()):
                    hp_list=hp_list[2:]
                    att_list=att_list[2:]
                    def_list=def_list[2:]
                    sp_att_list=sp_att_list[2:]
                    sp_def_list=sp_def_list[2:]
                    speed_list=speed_list[2:]
                    total_list=total_list[2:]
                #Sometimes the male and female versions of pokemon have different stats, this elif statement checks if this is the case and makes corrections to the type lists
                #And adds suffixes to the names in variant list differentiate them
                elif any('Male' and 'Female' in s for s in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/h5/span/text()').getall()):
                    t1_list=[t1_list[0], t1_list[0]]
                    t2_list=[t2_list[0], t2_list[0]]
                    variant_list=[pkm_name+' Male', pkm_name+ ' Female']
                    
                    
                else:
                    hp_list=hp_list[1::2]
                    att_list=att_list[1::2]
                    def_list=def_list[1::2]
                    sp_att_list=sp_att_list[1::2]
                    sp_def_list=sp_def_list[1::2]
                    speed_list=speed_list[1::2]
                    total_list=total_list[1::2]
                
            elif len(total_list)>len(variant_list):

                hp_list=hp_list[1:]
                att_list=att_list[1:]
                def_list=def_list[1:]
                sp_att_list=sp_att_list[1:]
                sp_def_list=sp_def_list[1:]
                speed_list=speed_list[1:]
                total_list=total_list[1:]
            
            else:
                dex_n=dex_n

                
                
            for pkm_var, hp_var, att_var, def_var, sp_att_var, sp_def_var, speed_var, total_var, t1, t2, img_url in zip(variant_list, hp_list, att_list, def_list, sp_att_list, sp_def_list, speed_list, total_list, t1_list, t2_list, img_list):
                Leg = False
                Myth = False
                UB = False
                Para = False
                Pseudo = False               
                    
                
                #Checks if there is any mention of the pokemon being part of these groups and sets them to true
                if 'Legendary Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall() or 'Legendary' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    Leg = True
                if 'Mythical Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    Myth = True
                if 'Ultra Beasts' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[3]/a/text()').getall():
                    UB = True
                if 'Paradox Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall() or 'Paradox' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    Para = True
                if 'pseudo-legendary Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    Pseudo = True

                if t1=='Unknown':
                    t1=t1_list[0]
                    t2=t2_list[0]
                        
                if pkm_var!=pkm_name:
                    if any(x in pkm_var for x in alt_forms):
                        pkm_var = pkm_name+' '+pkm_var
                        
                #Checks if the pokemon is a Mega version
                if 'Mega ' in pkm_var:
                    Mega = True
                else:
                    Mega = False
                #Checks if any of the keywords in the regional_forms list exist in the pokemons name
                if any(x in pkm_var for x in regional_forms):
                    Reg = True
                else:
                    Reg = False
                        
                    
                hp=hp_var
                att=att_var
                defense=def_var
                sp_att=sp_att_var
                sp_def=sp_def_var
                speed=speed_var
                total=total_var
                dex_n=dex_n.replace('#', '')
                filename = self.gen_filename(dex_n, pkm_var)
                                
                
                #if a pokemon does not have a second type it will be a string wiith 'Unknown' this checks for that and makes it None (keep in mind this is not a string)
                if t2=='Unknown':
                    t2=None
                
                #Converts the generation from string into integer
                if gen=='Generation I':
                    gen=1
                elif gen=='Generation II':
                    gen=2
                elif gen=='Generation III':
                    gen=3
                elif gen=='Generation IV':
                    gen=4
                elif gen=='Generation V':
                    gen=5
                elif gen=='Generation VI':
                    gen=6
                elif gen=='Generation VII':
                    gen=7
                elif gen=='Generation VIII':
                    gen=8
                elif gen=='Generation IX':
                    gen=9


                yield response.follow(img_url, callback=self.follow_image, meta={'filename': filename})

                    
                #yield the stats of the pokemon
                yield {
                    'Pokedex Number':dex_n,
                    'Base Pokemon': pkm_name,
                    'Variant Name': pkm_var,
                    'Type 1': t1,
                    'Type 2': t2,
                    'Total': total,
                    'HP': hp,
                    'Attack': att,
                    'Defense': defense,
                    'Sp. Atk': sp_att,
                    'Sp. Def': sp_def,
                    'Speed': speed,
                    'Generation': gen,
                    'Mega': Mega,
                    'Paradox': Para,
                    'Legendary': Leg,
                    'Pseudo-legendary': Pseudo,
                    'Ultrabeast': UB,
                    'Regional Form': Reg,
                    'Mythical': Myth,
                    'img_name': filename
                    }
            
        
        else:
            #variant_list= response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/a/@title').getall()
            print(variant_list)
            print(len(set(variant_list)), len(variant_list))
            if len(variant_list)-len(set(variant_list))>1:
                for i in range(1, len([x for x in variant_list if pkm_name in x])):
                    variant_list[i]= variant_list[i]+' ' + variant_list[i+1]
                    variant_list.remove(variant_list[i+1])
                variant_list= sorted(set([x for x in variant_list]), key=variant_list.index)
            
            print(variant_list)
            print(total_list)
            print(t1_list)
            
            if len(total_list) < len(variant_list):
                for i in range(0, (len(variant_list)-len(total_list))):
                    total_list.append(total_list[1])
                    hp_list.append(hp_list[1])
                    att_list.append(att_list[1])
                    def_list.append(def_list[1])
                    sp_att_list.append(sp_att_list[1])
                    sp_def_list.append(sp_def_list[1])
                    speed_list.append(speed_list[1])
                    
            for variant, hp_var, att_var, def_var, sp_att_var, sp_def_var, speed_var, total_var, t1, t2, img_url in zip(variant_list, hp_list, att_list, def_list, sp_att_list, sp_def_list, speed_list, total_list, t1_list, t2_list, img_list):
                
                Leg = False
                Myth = False
                UB = False
                Para = False
                Pseudo = False               
                    
                
                #Checks if there is any mention of the pokemon being part of these groups and sets them to true
                if 'Legendary Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall() or 'Legendary' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    Leg = True
                if 'Mythical Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    Myth = True
                if 'Ultra Beasts' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[3]/a/text()').getall():
                    UB = True
                if 'Paradox Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall() or 'Paradox' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    Para = True
                if 'pseudo-legendary Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    Pseudo = True
                
                
                
                if len(variant_list)==0:
                    variant_list=[pkm_name]
                if len(t1_list) > len(variant_list):
                    t1_list=t1_list[0:len(variant_list)]
                if len(t2_list) > len(variant_list):
                    t2_list=t2_list[0:len(variant_list)]
                
    
                if variant==pkm_name:
                    pkm_var=pkm_name
                    t1=t1_list[0]
                    t2=t2_list[0]
                elif variant!=pkm_name:
                    pkm_var=variant
                
                #Used to check if all forms of a Pokemon have the same type and if true sets the correct type for all forms of the pokemon
                if t1_list[1:]==t2_list[1:]:
                    t1=t1_list[0]
                    t2=t2_list[0]
                    
                    
                if 'Mega ' in pkm_var:
                    Mega = True
                else:
                    Mega = False

                if any(x in pkm_var for x in regional_forms):
                    Reg = True
                else:
                    Reg = False
                    
                
                hp=hp_var
                att=att_var
                defense=def_var
                sp_att=sp_att_var
                sp_def=sp_def_var
                speed=speed_var
                total=total_var
                dex_n=dex_n.replace('#', '')
                filename = self.gen_filename(dex_n, pkm_var)
                                
                
                if t2=='Unknown':
                    t2=None
                
                if gen=='Generation I':
                    gen=1
                elif gen=='Generation II':
                    gen=2
                elif gen=='Generation III':
                    gen=3
                elif gen=='Generation IV':
                    gen=4
                elif gen=='Generation V':
                    gen=5
                elif gen=='Generation VI':
                    gen=6
                elif gen=='Generation VII':
                    gen=7
                elif gen=='Generation VIII':
                    gen=8
                elif gen=='Generation IX':
                    gen=9


                yield response.follow(img_url, callback=self.follow_image, meta={'filename': filename})

                    
                yield {
                    'Pokedex Number':dex_n,
                    'Base Pokemon': pkm_name,
                    'Variant Name': pkm_var,
                    'Type 1': t1,
                    'Type 2': t2,
                    'Total': total,
                    'HP': hp,
                    'Attack': att,
                    'Defense': defense,
                    'Sp. Atk': sp_att,
                    'Sp. Def': sp_def,
                    'Speed': speed,
                    'Generation': gen,
                    'Mega': Mega,
                    'Paradox': Para,
                    'Legendary': Leg,
                    'Pseudo-legendary': Pseudo,
                    'Ultrabeast': UB,
                    'Regional Form': Reg,
                    'Mythical': Myth,
                    'img_name': filename
                    }

    def gen_filename(self, dex, var):
        var = var.replace(':', '').replace('%', '')
        filename = f'{dex}_{var}.png'
        return filename

    def follow_image(self, response):
        filename = response.meta['filename']
        img_href = response.css('#file > a:nth-child(1)').attrib['href']
        yield Request('https:'+img_href, callback=self.parse_image, meta={'filename': filename})

    def parse_image(self, response):
        filename = response.meta['filename']

        image_path = './img/'+filename

        with open(image_path, 'wb') as f:
            f.write(response.body)