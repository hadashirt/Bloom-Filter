from BitHash import BitHash 
from BitVector import BitVector

class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        #calculate the N,(the number of bits needed), using the equation
        phi=(1-((maxFalsePositive)**(1/numHashes)))
        N=numHashes/(1-(phi**(1/numKeys)))
        #return N as an int and add one so its rounded up 
        return int(N)+1
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        #numHashes
        self.__numHashes=numHashes
        #false positive rate
        self.__falsePos=maxFalsePositive
        #size
        self.__size = self.__bitsNeeded(numKeys,numHashes,maxFalsePositive)
        #bitVector
        self.__Vector=BitVector(size=self.__size)
        #keys inserted
        self.__nItems=0
      
    
     
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        ans=0
        prev=0
        #loop through the number of Hashes times 
        for i in range(self.__numHashes):
            #set ans to be the BitHash value 
            ans=BitHash(key,ans)
            final=BitHash(key,ans)%self.__size
            if self.__Vector[final]==0:
                #increment nItems by 1
                self.__nItems+=1
                #change the value from 0 to 1
                self.__Vector[final]=1
                
    
        
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        ans=0
        prev=0
        for i in range(self.__numHashes):
            ans=BitHash(key,ans)
            final=BitHash(key,ans)%self.__size
            #if a zero is found in the BitHash(final) loaction in Vector,then the key 
            #has not been inserted 
            if self.__Vector[final]==0:
                return False 
        return True
        
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 

    def falsePositiveRate(self):
        #calculate the proportion of bits currently in the bit vector that are 0 
        phi=(self.__size-self.numBitsSet())/self.__size
        #Calculating the P
        P=(1-phi)**self.__numHashes

        return P  
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    def numBitsSet(self):
        return self.__nItems
        


       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
   

    # create the Bloom Filter
    Bloom=BloomFilter(numKeys, numHashes, maxFalse)

    
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    fin = open("wordlist.txt")
    for i in range(numKeys):
        line=fin.readline()
        Bloom.insert(line)
    fin.close()
    
    
    # Print out what the PROJECTED false positive rate should 
    print("The Projected False Positive Rate is ",Bloom.falsePositiveRate()*100,"%")

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter.
    fin=open("wordlist.txt")
    ans=0
    for i in range(numKeys):
        line=fin.readline()
        if Bloom.find(line)==0:
            ans+=1
    print("There are ",ans, " missing from the first 100000 words")
        
    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    badans=0
    for i in range(numKeys,numKeys*2):
        line=fin.readline()
        if Bloom.find(line):
            badans+=1
            
    # Print out the percentage rate of false positives.
    print("The percentage rate of false positives is ",(badans/numKeys)*100,"%")
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE

    
if __name__ == '__main__':
    __main()       

