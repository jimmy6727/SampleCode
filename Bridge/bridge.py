from redeal import *
from dds import *
import statistics

def PrintHCPvsFibHCP(deal):
    print(deal._long_str())
    print("North HCP: " +str(deal.north.hcp) + "\t   North Fibonacci HCP: " +str(deal.north.fibhcp))
    print("East HCP: " +str(deal.east.hcp) + "\t   North Fibonacci HCP: " +str(deal.east.fibhcp))
    print("South HCP: " +str(deal.south.hcp) + "\t   North Fibonacci HCP: " +str(deal.south.fibhcp))
    print("West HCP: " +str(deal.west.hcp) + "\t   North Fibonacci HCP: " +str(deal.west.fibhcp))
    print("\n")
    print("N/S HCP: " + str(deal.north.hcp+deal.south.hcp) + "\t   N/S Fibonacci HCP: " + str(deal.north.fibhcp+deal.south.fibhcp))
    print("E/W HCP: " + str(deal.east.hcp+deal.west.hcp) + "\t   E/W Fibonacci HCP: " + str(deal.east.fibhcp+deal.west.fibhcp))
    print("\n")
    
def SolveAndPrintForEachLead(deal, strain, declarer):
    # pass a redeal Deal object, strain "C" "D" "H" "S" "N", and declarer "N" "S" "E" "W"
    # Returns a dictionary in the form a[Lead Card] : DD Tricks taken
    
    # Set leader
    if declarer == "N":
        l = "E"
    elif declarer == "S":
        l = "W"
    elif declarer == "E":
        l = "N"
    elif declarer == "W":
        l = "S"
        
    a = dds.solve_all(deal, strain, l)
    #print("## Result for above deal with " +str(strain) + " contract with " +str(declarer) + " as declarer. ##\n")
    lead_tricks = {}
    for c in a.items():
        lead_tricks[str(c[0])] = 13-c[1]
        #print("Lead: " + str(c[0]) + "   N/S DD Tricks taken: " + str(13-c[1]))
    
    return lead_tricks

def MakeGame(lead_tricks_dict, game_tricks):
    #print(lead_tricks_dict)
#    make = 0
#    for tx in lead_tricks_dict.values():
#        if tx >= game_tricks:
#            make += 1
#    print("Makes game on " + str(100*make/len(lead_tricks_dict)) + " percent of leads")
    tricks = min(lead_tricks_dict.values())
    #print(tricks)
    if tricks >= game_tricks:
        return(True)


# This accept function represents a 1NT opening from north
# Balance and stopping at a minor suit
# Honors in sequence
def accept(deal):
    if ((balanced(deal.north)) and 
        15 <= deal.north.hcp <= 17 and 
        deal.north.hcp + deal.south.hcp == 25):
        return(deal)
        
def HSP_NT(deal):
    global hcp
    if ((balanced(deal.north)) and 
        15 <= deal.north.hcp <= 17 and 
        deal.north.hcp + deal.south.hcp == hcp):
        return deal
    
def HSP_Major(deal):
    global hcp
    global strain
    if strain == "H":
        if ((len(deal.north.hearts)+len(deal.south.hearts)) >= 8 and 
            deal.north.hcp + deal.south.hcp == hcp):
            return deal
    if strain == "S":
        if ((len(deal.north.spades)+len(deal.south.spades)) >= 8 and 
            deal.north.hcp + deal.south.hcp == hcp):
            return deal

def HSP_NT_LT1(deal):
    global hcp
    if ((balanced(deal.north)) and 
        15 <= deal.north.hcp <= 17 and 
        deal.north.hcp + deal.south.hcp == hcp and
        deal.north.hsp + deal.south.hsp <=1):
        return deal
       
def HSP_NT_MT3(deal):
    global hcp
    if ((balanced(deal.north)) and 
        15 <= deal.north.hcp <= 17 and 
        deal.north.hcp + deal.south.hcp == hcp and
        deal.north.hsp + deal.south.hsp >= 3):
        return deal
    
def MajorHSPLessThan1(deal):
    global hcp
    global strain
    if strain == "H":
        if ((len(deal.north.hearts)+len(deal.south.hearts)) >= 8 and 
            deal.north.hcp + deal.south.hcp == hcp and
            deal.north.hsp + deal.south.hsp <=1):
            return deal
    if strain == "S":
        if ((len(deal.north.spades)+len(deal.south.spades)) >= 8 and 
            deal.north.hcp + deal.south.hcp == hcp and
            deal.north.hsp + deal.south.hsp <=1):
            return deal

        
def MajorHSPMoreThan3(deal):
    global hcp
    global strain
    if strain == "H":
        if ((len(deal.north.hearts)+len(deal.south.hearts)) >= 8 and 
            deal.north.hcp + deal.south.hcp == hcp and
            deal.north.hsp + deal.south.hsp >= 3):
            return deal
    if strain == "S":
        if ((len(deal.north.spades)+len(deal.south.spades)) >= 8 and 
            deal.north.hcp + deal.south.hcp == hcp and
            deal.north.hsp + deal.south.hsp >= 3):
            return deal
    
strain = "H"
n = 1000
    
for hcp in range(20,29):

    s = 0
    x = 0
    less = []
    more = []
    l = []
    hsp_values_made_game = []
    hsp_values_not_made_game = []
    print("\n N/S HCP: " + str(hcp))
    for i in range(n):
        
        dealer = redeal.Deal.prepare()
    
        # Generate a deal using our accept function above
        Mdeal = dealer(accept_func = HSP_Major)
       # Mdeal1 = dealer(accept_func = MajorHSPMoreThan3)
        
    #    PrintHCPvsFibHCP(Mdeal)
        a = SolveAndPrintForEachLead(Mdeal, strain, "N")
        #b = SolveAndPrintForEachLead(Mdeal1, strain, "N")
        
        f = Mdeal.north.fibhcp+Mdeal.south.fibhcp
        #g = Mdeal1.north.fibhcp+Mdeal1.south.fibhcp
        
        l.append(f)
        
        if MakeGame(a,10) == True:
            s += 1
            hsp_values_made_game.append(Mdeal.north.hsp+Mdeal.south.hsp)
        else:
            hsp_values_not_made_game.append(Mdeal.north.hsp+Mdeal.south.hsp)
            
#        if MakeGame(b,10) == True:
#            x += 1
#            hsp_values_made_game.append(Mdeal.north.hsp+Mdeal.south.hsp)
#        else:
#            hsp_values_not_made_game.append(Mdeal.north.hsp+Mdeal.south.hsp)
#    
#    print("Made games percentage when HSP 1 or less: " + str(s/n))
#    print("Made games percentage when HSP 3 or more: " + str(x/n))
    print("Made games percentage: " + str(s/n))
    print("Average N/S fibHCP: " + str(statistics.mean(l)))
    print("Average HSP for made games: " + str(statistics.mean(hsp_values_made_game)))
    print("Average HSP for not made games: " + str(statistics.mean(hsp_values_not_made_game)))
    
    
    