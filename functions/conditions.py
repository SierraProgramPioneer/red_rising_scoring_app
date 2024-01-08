# Import Character Class Functions
from functions.classes.golds import *
from functions.classes.silvers import *
from functions.classes.whites import *
from functions.classes.coppers import *
from functions.classes.blues import *
from functions.classes.yellows import *
from functions.classes.greens import *
from functions.classes.violets import *
from functions.classes.oranges import *
from functions.classes.grays import *
from functions.classes.browns import *
from functions.classes.obsidians import *
from functions.classes.pinks import *
from functions.classes.reds import *


# Function Map (Converts Character Name to Valid Function Name)

function_map = {
'4D Painter' : four_d_painter,
'Administrator' : administrator,
'Aegis Craftsman' : aegis_craftsman,
'Aja' : aja,
'Alfrun' : alfrun,
'Alia Snow Sparrow' : alia_snow_sparrow,
'Antonia' : antonia,
'Arlus' : arlus,
'Artificer' : artificer,
'Artisan Chef' : artisan_chef,
'Ash Lord' : ash_lord,
'Assassin' : assassin,
'Auctioneer' : auctioneer,
'Banker' : banker,
'Bondilus' : bondilus,
'Bone Riders' : bone_riders,
'Bridge' : bridge,
'Calliope' : calliope,
'Cassius' : cassius,
'CEO' : ceo,
'Codebreaker' : codebreaker,
'Colonel Valentin' : colonel_valentin,
'Conversationalist' : conversationalist,
'Cyther' : cyther,
'Dancer' : dancer,
'Danto' : danto,
'Darrow' : darrow,
'Dataport Specialist' : dataport_specialist,
'Deanna' : deanna,
'Developer' : developer,
'Diplomat' : diplomat,
'Dr. Virany' : dr_virany,
'Eo' : eo,
'Evey' : evey,
'Firewall Expert' : firewall_expert,
'Fitchner' : fitchner,
'Garden-Trained Rose' : garden_trained_rose,
'Gardener' : gardener,
'Gravboot Cobbler' : gravboot_cobbler,
'Group Counselor' : group_counselor,
'Hacker' : hacker,
'Harmony' : harmony,
'Helga' : helga,
'Holiday' : holiday,
'Holo Designer' : holo_designer,
'Holo Host' : holo_host,
'Hypnotist' : hypnotist,
'Investor' : investor,
'Invictus' : invictus,
'Janitor' : janitor,
'Jopho' : jopho,
'Judge' : judge,
'Justice' : justice,
'Karnus' : karnus,
'Lawyer' : lawyer,
'Loan Shark' : loan_shark,
'Lorn' : lorn,
'Lysander' : lysander,
'Magistrate' : magistrate,
'Martyr' : martyr,
'Masseuse' : masseuse,
'Matteo' : matteo,
'Mess Hall Cook' : mess_hall_cook,
'Mickey the Carver' : mickey_the_carver,
'Modjob' : modjob,
'Morning Star' : morning_star,
'Musician' : musician,
'Mustang' : mustang,
'Nanny' : nanny,
'Nero' : nero,
'Octavia' : octavia,
'Online Gambler' : online_gambler,
'Orator' : orator,
'Orion' : orion,
'Pathologist' : pathologist,
'Pax Au Telemanus' : pax_au_telemanus,
'Pelus' : pelus,
'Politician' : politician,
'Priestess' : priestess,
'Psychologist' : psychologist,
'Pulse Armorer' : pulse_armorer,
'Pulse Fist Engineer' : pulse_fist_engineer,
'Quicksilver' : quicksilver,
'Quietus' : quietus,
'Ragnar' : ragnar,
'Razor Designer' : razor_designer,
'Reporter' : reporter,
'Researcher' : researcher,
'Romulus' : romulus,
'Roque' : roque,
'Seer' : seer,
'Sefi' : sefi,
'Sevro' : sevro,
'Sponsor' : sponsor,
'Stained' : stained,
'Stock Broker' : stock_broker,
'Sun-Hwa' : sun_hwa,
'Surgeon' : surgeon,
'Tactus' : tactus,
'The Howlers' : the_howlers,
'The Jackal' : the_jackal,
'The Pax' : the_pax,
'The Telemanuses' : the_telemanuses,
'Theodora' : theodora,
'Timony' : timony,
'Trigg' : trigg,
'Ugly Dan' : ugly_dan,
'Uncle Narol' : uncle_narol,
'Victra' : victra,
'Virga' : virga,
'Vlogger' : vlogger,
'Zanzibar' : zanzibar,
}