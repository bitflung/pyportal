import time

class SmartTouch:
    """A smart object to collect touch point information"""
    # consider: track maxZ observed and set minZ to 25% of maxZ
    
    minZ=15000; # default minimum touch pressure
    proximity=20; # default minimum proximity in pixels (square; used for both x and y)
    
    consecutiveSamps=4; # default number of consecutive valid samples for a touch point to be captured    
    currentSamples=[0,0,0,0,0,0,0,0]; # dynamic list size? oh python you confound me. using static for now
    currentIndex=0;
    
	tscreen;
	
    dbgLvl=0;
    
    def __init__(self):
		self.tscreen=None;
        self.zeroize();
    
    def debug(self, *args):
        self.debugLvl(2, args);
        
    def debugLvl(self, lvl, *args):
        if(lvl <= self.dbgLvl):
            print(args);
            
    def zeroize(self):
        self.debug("      * zeroizing...");
        zeroSample=(0,0,0);
        i=0;
        while(i<self.consecutiveSamps):
            self.currentSamples[i]=zeroSample;
            i=i+1;
            
        self.currentIndex=0;
        
	def setTscreen(tscreen):
		self.tscreen=tscreen;
		
	def poll():
		touching=False;
		valid=False;
		
		if(not self.tscreen):
			self.debug("ERROR: touch screen object not yet defined!");
			return touching, valid; # False, False
			
		try:
			tp=self.tscreen.touch_point;
		except:
			self.debug("touchscreen input failure");
			tp=None;
			time.sleep(1); # pause the loop for a second since the screen is acting poorly
			return touching, valid; # False, False
			
		if(tp)
			touching=True;
		
		valid=self.push(tp);
		
		return touching, valid; # dynamic booleans
			
    def push(self, tp):        
        if(tp):
            if(self.currentIndex>=self.consecutiveSamps):
                return True; # exit early if we've already collected enough data
        
            # valid tp tuple; test minZ
            if(tp[2]>=self.minZ):
                self.debugLvl(1, "RX TP: ", tp);
                #print("TP satisfies minZ");
                
                if(self.test(tp)):
                    self.debugLvl(1, "   > TP is valid (within proximity)");
                    # if this touchpoint is WITHIN PROXIMITY LIMITS, extend the data set
                    self.currentSamples[self.currentIndex]=tp;
                    self.currentIndex=self.currentIndex+1;
                else:
                    self.debugLvl(0, "   < TP is invalid (outside proximity)", tp);
                    # if this touchpoint is OUTSIDE PROXIMITY LIMITS, zeroize and wait for the next touch
                    self.zeroize();
            else:
                # doesn't satisfy minZ, so IGNORE IT (don't zeroize!)
                self.debugLvl(1, "RX'd TP below minZ: ", tp);
                
            #self.debugLvl(1, "   currentIndex: ", self.currentIndex);
            #self.debugLvl(1, "   currentSamples:\r\n", self.currentSamples);
            return(self.currentIndex >= self.consecutiveSamps);
        else:
            return False; # return value indicates when we are done
        
    def test(self, tp):
        # test against minZ in the push() function so we can differentiate between
        # fails due to minZ and fails due to x/y proximity
        #if(tp[2] < self.minZ):
        #    return False;
        #else:
        #    print("TP satisfies minZ");
            
        if(self.currentIndex==0):
            self.debug("   TP is first sample; always passes test");
            return True; # always accept the first sample
        else:
            self.debug("   testing against average x/y locale");
            
        pprox=self.proximity;
        nprox=(-1)*self.proximity;
        
        avgSamp=self.getAvgPosition();
        self.debug("        avgSamp x,y: ", avgSamp[0], avgSamp[1]);
        xDif=avgSamp[0]-tp[0];
        yDif=avgSamp[1]-tp[1];
        self.debug("        xDif, yDif: ", xDif, yDif);
        
        if(xDif > pprox):
            return False;
        if(xDif < nprox):
            return False;
        if(yDif > pprox):
            return False;
        if(yDif < nprox):
            return False;
        
        # we've filtered for minZ, x-proximity, and y-proximity
        # so if we reach this line the touchpoint is VALID and the test PASSES
        return True;
        
    def getAvgPosition(self):
        avgX=0;
        avgY=0;
        i=0;
        while(i<self.currentIndex):
            tmpSamp=self.currentSamples[i];
            avgX=avgX+tmpSamp[0];
            avgY=avgY+tmpSamp[1];
            i=i+1;
            
        avgX=avgX/(self.currentIndex);
        avgY=avgY/(self.currentIndex);
        
        #avgX=math.floor(avgX);
        #avgY=math.floor(avgY);
        
        return (avgX, avgY, self.minZ); # return a touchpoint tuple with > minZ pressure value
    
    def consume(self):
        ret = self.getAvgPosition();
        self.zeroize();
        self.debugLvl(1, "avgSamp: ", ret);
        return ret;
