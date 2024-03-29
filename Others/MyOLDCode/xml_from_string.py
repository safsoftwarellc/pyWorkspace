import lxml.etree as ET
from io import StringIO

xml_string = '''<?xml version="1.0" encoding="UTF-8"?><!--
  == Copyright (c) 2002-2009. All rights reserved.
  == Financial Products Markup Language is subject to the FpML public license.
  == A copy of this license is available at http://www.fpml.org/license/license.html
  --><!--
  == This examples shows how to represent Credit Event Notice as notification message
  -->
<FpML xmlns="http://www.fpml.org/2009/FpML-4-6" xmlns:fpml="http://www.fpml.org/2009/FpML-4-6" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="4-6" xsi:type="CreditEventNotification" xsi:schemaLocation="http://www.fpml.org/2009/FpML-4-6 ../fpml-main-4-6.xsd http://www.w3.org/2000/09/xmldsig# ../xmldsig-core-schema.xsd">
   <header>
      <messageId messageIdScheme="http://www.example.com/messageId">CEN/2004/01/05/15-38</messageId>
      <sentBy>GSI</sentBy>
      <sendTo>ABC</sendTo>
      <creationTimestamp>2004-01-05T15:38:00Z</creationTimestamp>
   </header>
   <creditEventNotice>
      <affectedTransactions>
         <tradeReference>
            <partyTradeIdentifier>
               <partyReference href="party1"/>
               <tradeId tradeIdScheme="http://www.gs.com/fpmltid">1234ABCD</tradeId>
            </partyTradeIdentifier>
         </tradeReference>
      </affectedTransactions>
      <referenceEntity id="referenceEntity">
         <entityName>Solutia Inc.</entityName>
         <entityId entityIdScheme="http://www.fpml.org/spec/2003/entity-id-RED-1-0">8G836J</entityId>
      </referenceEntity>
      <bankruptcy/>
      <publiclyAvailableInformation>
         <resourceId resourceIdScheme="http://www.bankA.com/cen/resource">GS-CEN_Resource-001</resourceId>
         <language languageScheme="http://www.fpml.org/ext/ISO-639-2T">eng</language>
         <sizeInBytes>505</sizeInBytes>
         <length>
            <lengthUnit>Pages</lengthUnit>
            <lengthValue>1</lengthValue>
         </length>
         <mimeType mimeTypeScheme="http://www.fpml.org/ext/RFC2046">text/html</mimeType>
         <name>AP-Solutia.html</name>
         <comments>Also available in PDF format.</comments>
         <url>http://www.nytimes.com/aponline/business/AP-Solutia.html</url>
      </publiclyAvailableInformation>
      <notifyingPartyReference href="party1"/>
      <notifiedPartyReference href="party2"/>
      <creditEventNoticeDate>2004-01-05Z</creditEventNoticeDate>
      <creditEventDate>2003-12-17Z</creditEventDate>
   </creditEventNotice>
   <party id="party1">
      <partyId>GSI</partyId>
      <partyName>Goldman Sachs International</partyName>
   </party>
   <party id="party2">
      <partyId>ABC</partyId>
      <partyName>BANK ABC Co.</partyName>
   </party>
</FpML>'''

xml = '<a xmlns="test"><b xmlns="test"/></a>'

parser = ET.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

root = ET.parse(xml_string.encode('utf8'), parser).getroot()
print(root)
