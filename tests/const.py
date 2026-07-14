"""Shared constants and fixtures for Green Button tests."""

from __future__ import annotations

# A minimal-but-complete ESPI (Green Button) Atom feed containing exactly one
# UsagePoint, linked to a MeterReading, which is in turn linked to a ReadingType
# and a single IntervalBlock with one IntervalReading. This mirrors the shape
# that ``custom_components.green_button.parsers.espi`` expects.
VALID_ESPI_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:espi="http://naesb.org/espi">
  <entry>
    <link rel="self" href="/UsagePoint/1"/>
    <link rel="related" href="/UsagePoint/1/MeterReading/1"/>
    <content>
      <espi:UsagePoint>
        <espi:ServiceCategory>
          <espi:kind>0</espi:kind>
        </espi:ServiceCategory>
      </espi:UsagePoint>
    </content>
  </entry>
  <entry>
    <link rel="self" href="/UsagePoint/1/MeterReading/1"/>
    <link rel="related" href="/UsagePoint/1/MeterReading/1/ReadingType/1"/>
    <link rel="related" href="/UsagePoint/1/MeterReading/1/IntervalBlock/1"/>
    <content>
      <espi:MeterReading/>
    </content>
  </entry>
  <entry>
    <link rel="self" href="/UsagePoint/1/MeterReading/1/ReadingType/1"/>
    <content>
      <espi:ReadingType>
        <espi:powerOfTenMultiplier>0</espi:powerOfTenMultiplier>
        <espi:uom>72</espi:uom>
        <espi:currency>840</espi:currency>
      </espi:ReadingType>
    </content>
  </entry>
  <entry>
    <link rel="self" href="/UsagePoint/1/MeterReading/1/IntervalBlock/1"/>
    <content>
      <espi:IntervalBlock>
        <espi:interval>
          <espi:start>1609459200</espi:start>
          <espi:duration>3600</espi:duration>
        </espi:interval>
        <espi:IntervalReading>
          <espi:cost>1000</espi:cost>
          <espi:timePeriod>
            <espi:start>1609459200</espi:start>
            <espi:duration>3600</espi:duration>
          </espi:timePeriod>
          <espi:value>100</espi:value>
        </espi:IntervalReading>
      </espi:IntervalBlock>
    </content>
  </entry>
</feed>
"""

# The unique ID (UsagePoint self href) produced by parsing ``VALID_ESPI_XML``.
VALID_USAGE_POINT_ID = "/UsagePoint/1"

# A well-formed Atom feed that contains no UsagePoint entries.
EMPTY_FEED_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:espi="http://naesb.org/espi">
</feed>
"""

# Not valid XML at all.
INVALID_XML = "this is not xml"
