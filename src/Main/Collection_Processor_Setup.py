from string import Template
from pathlib import Path

COLLECTION_PROCESSOR_SETUP_XML= """<?xml version="1.0" encoding="UTF-8"?>

    <!--
     ***************************************************************
     * Licensed to the Apache Software Foundation (ASF) under one
     * or more contributor license agreements.  See the NOTICE file
     * distributed with this work for additional information
     * regarding copyright ownership.  The ASF licenses this file
     * to you under the Apache License, Version 2.0 (the
     * "License"); you may not use this file except in compliance
     * with the License.  You may obtain a copy of the License at
         *
     *   http://www.apache.org/licenses/LICENSE-2.0
     * 
     * Unless required by applicable law or agreed to in writing,
     * software distributed under the License is distributed on an
     * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
     * KIND, either express or implied.  See the License for the
     * specific language governing permissions and limitations
     * under the License.
     ***************************************************************
   -->
   
<cpeDescription>
    <collectionReader>
        <collectionIterator>
            <descriptor>
                <import location="./Setup_CPE.xml"></import>
            </descriptor>
        </collectionIterator>
    </collectionReader>
    <casProcessors casPoolSize="$CAS_POOL_SIZE" processingUnitThreadCount="$THREADS">
        <casProcessor deployment="integrated" name="Sentence Aggregate">
            <descriptor>
                <import location="./DoNothing.xml"></import>
            </descriptor>
            <deploymentParameters></deploymentParameters>
            <filter></filter>
            <errorHandling>
                <errorRateThreshold action="terminate" value="0/1000"/>
                <maxConsecutiveRestarts action="terminate" value="1"></maxConsecutiveRestarts>
                <timeout max="100000"/>
            </errorHandling>
            <checkpoint batch="10000"></checkpoint>
        </casProcessor>
    </casProcessors>
    <cpeConfig>
        <numToProcess>-1</numToProcess>
        <deployAs>immediate</deployAs>
        <checkpoint file="" time="300000"/>
        <timerImpl></timerImpl>
    </cpeConfig>
</cpeDescription>
"""

def generate_collection_processor_setup(output_file, cas_pool_size, threads):
    """output_file: a pathlib object"""
    s = Template(COLLECTION_PROCESSOR_SETUP_XML)
    ret = s.substitute(CAS_POOL_SIZE=cas_pool_size, THREADS=threads)
    with output_file.open(mode="w") as out_file:
        out_file.write(ret)

      