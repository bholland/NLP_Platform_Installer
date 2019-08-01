from string import Template

DoNothing = """<?xml version="1.0" encoding="UTF-8"?>
<analysisEngineDescription xmlns="http://uima.apache.org/resourceSpecifier">
    
  <frameworkImplementation>org.apache.uima.java</frameworkImplementation>
    
  <primitive>true</primitive>
    
  <annotatorImplementationName>annotators.DoNothing</annotatorImplementationName>
    
  <analysisEngineMetaData>
        
    <name>DoNothing</name>
        
    <description>
      This does nothing. It is here as a placeholder for collection readers that require absolutely nothing to happen to their collections. This is very useful for ingesting documents. 
    </description>
        
    <version>1.0</version>
        
    <vendor/>
        
    <configurationParameters/>
        
    <configurationParameterSettings/>
        
    <typeSystemDescription/>
        
    <fsIndexCollection/>
        
    <capabilities>
            
      <capability>
                
        <inputs/>
                
        <outputs/>
                
        <languagesSupported/>
              
      </capability>
          
    </capabilities>
        
    <operationalProperties>
            
      <modifiesCas>false</modifiesCas>
            
      <multipleDeploymentAllowed>false</multipleDeploymentAllowed>
            
      <outputsNewCASes>false</outputsNewCASes>
          
    </operationalProperties>
      
  </analysisEngineMetaData>
    
  <resourceManagerConfiguration/>
  
</analysisEngineDescription>

"""
def generate_do_nothing(output_file):
    """output_file: a pathlib object"""
    s = Template(DoNothing)
    ret = s.substitute()
    with output_file.open(mode="w") as out_file:
        out_file.write(ret)
    
    
      