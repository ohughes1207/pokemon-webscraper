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

TODO: Fix naming unable to deal with some unicode characters


TODO: Fix outliers

Darmanitan
Pikachu
Flabebe (unicode character error)




TODO: make method to add variant names to Zacian and Zamazenta

'''


import scrapy

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
    
    def parse(self, response):
        tables = response.css('table.roundy')
        
        for table in tables:
            all_pkm = table.xpath('tbody/tr')[1:]
            #all_pkm = [all_pkm[0]]
            for pkm in all_pkm:

                dex_n = pkm.xpath('td[1]//text()').get()
                #print(dex_n)
                if dex_n is not None and dex_n!='#0000':
                    print(dex_n)
                    pkm_link=pkm.xpath('td[3]/a/@href').get()
                    yield response.follow(pkm_link, callback= self.get_pkms)
                else:
                    continue
                
            


    def get_pkms(self, response):
        
        gen= [x for x in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall() if 'Generation' in x][0]
        #print(gen)
        dex_n = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/th/big/big/a/span/text()').get()
        #print(dex_n)
        pkm_name = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/big/big/b/text()').get()
        #print(pkm_name)
        t1_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[1]/a/span/b/text()').getall()
        #print(t1_main)
        t2_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/a/span/b/text()').getall()
        #print(t2_main)
        
        variant_list = [x for x in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/small/text()').getall() if 'Gigantamax' not in x]# if pkm_name in x] #and 'Gigantamax' not in x]
        
        if len(variant_list)==0:
            variant_list=[pkm_name]
        
        
        hp_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[3]/th/div[2]/text()').getall()
        att_list =  response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[4]/th/div[2]/text()').getall()
        def_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[5]/th/div[2]/text()').getall()
        sp_att_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[6]/th/div[2]/text()').getall()
        sp_def_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[7]/th/div[2]/text()').getall()
        speed_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[8]/th/div[2]/text()').getall()
        
        regional_forms = ['Paldean', 'Hisuian', 'Galarian', 'Alolan']
        alt_forms = [' Form', ' Mode', ' Build', 'Crowned', 'Hero ', ' Style', 'Family ', 'Normal', 'Size', 'Plumage', 'Breed', 'Cloak']
        
        total_list = response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/table/tbody/tr[9]/th/div[2]/text()').getall()
        
        
        '''
        if len(variant_list)==1:
            hp_list=hp_list[0]
            att_list=att_list[0]
            def_list=def_list[0]
            sp_att_list=sp_att_list[-1]
            sp_def_list=sp_def_list[-1]
            speed_list=speed_list[-1]
            total_list=total_list[-1]
        '''
        
        '''
        if len(total_list) > len(variant_list):          
            variant_list = [pkm_name+' (REQUIRES MANUAL ATTENTION)' for x in total_list]
        '''
        
        print(variant_list)
                    
        
        
        '''
        form_forms = [x for x in variant_list if pkm_name not in x]
        print('#################################################',  '\n', form_forms)
        '''
        if len(t1_list) > len(variant_list):
            t1_list=t1_list[0:len(variant_list)]
        if len(t2_list) > len(variant_list):
            t2_list=t2_list[0:len(variant_list)]
        

        #This method works for most however some stats and variants need correcting, such as Cosplay Pikachu and Mega Beedrill
        if len(t1_list)==len(variant_list):
            
            
            #Outliers in this if statement are Darmanitan, Pikachu and Flabebe
            if len(total_list) < len(variant_list):
                for i in range(1, len(variant_list)):
                    
                    
                    hp_list=hp_list+hp_list
                    att_list=att_list+att_list
                    def_list=def_list+def_list
                    sp_att_list=sp_att_list+sp_att_list
                    sp_def_list=sp_def_list+sp_def_list
                    speed_list=speed_list+speed_list
                    total_list=total_list+total_list
                    
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

                
            #variant_list= list(set([x.replace('(', '').replace(')', '') for x in variant_list]))
                
            for pkm_var, hp_var, att_var, def_var, sp_att_var, sp_def_var, speed_var, total_var, t1, t2 in zip(variant_list, hp_list, att_list, def_list, sp_att_list, sp_def_list, speed_list, total_list, t1_list, t2_list):
                
                    
                group = []
                    
                if any('Legendary' in s for s in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall()):
                        group.append('Legendary')
                elif any('Mythical' in s for s in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall()):
                        group.append('Mythical')
                elif any('Ultra Beasts' in s for s in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[3]/a/text()').getall()):
                        group.append('Ultra Beast')
                if any('Paradox' in s for s in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall()):
                        group.append('Paradox')
                    
                if t1=='Unknown':
                    t1=t1_list[0]
                    t2=t2_list[0]
                        
                if pkm_var!=pkm_name:
                    if any(x in pkm_var for x in alt_forms):
                        pkm_var = pkm_name+' '+pkm_var
                        
                        
                if 'Mega ' in pkm_var:
                        group.append('Mega')
                if any(x in pkm_var for x in regional_forms):
                        group.append('Regional Form')
                if len(group)==0:
                        group.append('Standard')
                        
                    
                hp=hp_var
                att=att_var
                defense=def_var
                sp_att=sp_att_var
                sp_def=sp_def_var
                speed=speed_var
                total=total_var
                
                print(pkm_var)
                
                
                
                
                
                
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
        
                    
                    
                    
                yield {
                    'Pokedex Number':dex_n.replace('#', ''),
                    'Pokemon': pkm_var.replace('\xa0', ' ').replace('♀', ' Female').replace('♂', ' Male'),
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
                    'Group': group,
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
                    
            for variant, hp_var, att_var, def_var, sp_att_var, sp_def_var, speed_var, total_var, t1, t2 in zip(variant_list, hp_list, att_list, def_list, sp_att_list, sp_def_list, speed_list, total_list, t1_list, t2_list):
                
                group = []
                
                if 'Legendary Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    group.append('Legendary')
                elif 'Mythical Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    group.append('Mythical')
                elif 'Ultra Beasts' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[3]/a/text()').getall():
                    group.append('Ultra Beast')
                elif 'Paradox Pokémon' in response.xpath('/html/body/div[2]/div[1]/div[1]/div[6]/div[4]/div/p[1]/a/text()').getall():
                    group.append('Paradox')
                
                
                
                
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
                    group.append('Mega')
                if any(x in pkm_var for x in regional_forms):
                    group.append('Regional Form')
                if len(group)==0:
                    group.append('Standard')
                    
                
                hp=hp_var
                att=att_var
                defense=def_var
                sp_att=sp_att_var
                sp_def=sp_def_var
                speed=speed_var
                total=total_var
    
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
    
                
                
                yield {
                    'Pokedex Number': int(dex_n.replace('#', '')),
                    'Pokemon': pkm_var.replace('(', '').replace(')', ''),
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
                    'Group': group,
                    }