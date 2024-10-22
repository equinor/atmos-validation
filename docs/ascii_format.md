# ASCII format

The ASCII format is only applicable for measurements. Hindcasts or single point hindcasts shall be delivered in netCDF (See [conventions](./conventions.md) for details).

ASCII format contains three sections: Common Metadata, Parameters Related Metadata and Data. See [example](../examples/example_ascii_measurement.dat) for a template to follow.

## Common Metadata

Common Metadata shall be given in the header lines of the timeseries. All header lines must start with a percentage symbol, %. There shall be one space between the percentage sign and the following text. There shall be minimum two spaces after ‘:’ in each line of the header. In case of missing data "NA" should be used.

The following metadata shall be included in all Metocean timeseries:

- **Contractor/Data Responsible**: Name of data provider
- **Project name**: Name of the project requesting data
- **Location**: Latitude and longitude of the measurements in degrees (at least three decimals are required after ‘.’) and corresponding reference datum. Format of the location: "% Location: lat lon, reference"
- **Duration of data**: Start and end dates of the measurements in format dd.mm.yyyy -dd.mm.yyyy (Dates shall be in UTC and agree with Start and End dates of the data).
- **Averaging period**: Averaging period of measurements in minutes
- **TotalWaterDepth**: Total water depth in meters. For wind data total water depth is NA
- **Mooring Name**: The mooring name shall be unique for each delivered measurement file (across projects, instruments, data deliveries etc) and shall be constructed as follows: project_name + mooring_name + instrument + phase. FOXTROT_MOOR1_GPS_Ph1. Only put single instrumentation in the name in cases where there are multiple instruments
- **Type of instrument**: Types of instruments used for the measurement location. If there are several instrument types, please, list them with comma separator. If there are no instruments available, use NA. Instrument types shall be chosen from the database list <https://atmos.app.radix.equinor.com/config/instrument-types>. If appropriate type is not available, please, contact CR to include it in the database
- **Specification of Instrument**: Instrument specifications for given measurement locations. Instrument specifications shall be listed in the same order as the corresponding instrument types
- **Measurement installation type**: Measurement installation type. One of the options listed in <https://atmos.app.radix.equinor.com/config/installation-types> database shall be specified
- **QC provider**: Company responsible for the QC. It can be different from the contractor.
- **Data Usability Level**: Level of the data readiness. One or more options from https://atmos.app.radix.equinor.com/config/data-usability shall be chosen. These metadata reflect how good the data are.
- **Data history**: Any information about the origin of the data (if not measured directly by the contractor) or changes made to the data (if there has been previous versions of the same data) shall be stated here. If the data has been measured directly by the contractor and it is the first version delivered “Original data” shall be stated.
- **Missing data**: Element reflecting missing data in the measurements shall be stated. NaN is preferred.
- **Final Reports**: A list of report file names, separated by comma, shall be provided. All stated report files shall follow the data
- **Data type**: word ‘Measurement’ shall be stated in this field
- **Classification level**: Signifies data access according to classification level: Open, Internal or Restricted
- **Comments**: Any relevant comments related to how the data has been treated shall be provided. It could be basic preprocessing steps etc
- **Asset**: Name of the asset which paid for the data. In case of sharing data to the third party, permission from the asset is required. NA can be used if asset is not applicable
- **Country**: Country name on which territory data are acquired. In case of sharing data to the third party, one need obey to country regulation rules related to data sharing
- **Auxilary information**: Other information about measurements shall be specified in the section below line % Comments . Format shall be similar as in the section above: Each line starts with a % sign and the metadata name shall be separated from the content by ‘:’ The metadata names in this section can be specified by the data provider.

## Parameter Related Metadata

Parameter Related Metadata shall be given in a table. Each line of the table shall be started from % sign.  The content of the table shall list all the measurement parameters and their metadata, therefore the number of rows of this table should be equal to the number of data columns in the in the Data section.  The metadata of each parameter except time quantities shall contain the following attributes indicated as a header of the table (See ASCII example):

- **Parameters**: Description of the measured quantity.
- **Abbrev**: Short name of the measured quantity. This name will be used in the data table as a header. Therefore, each abbreviation shall be unique in the entire file. Abbrev for the measured parameters shall be constructed as the key from the database with standardized parameter names (see Section 5.3) and absolute value of height/depth. For example, WS100, WD100, CS10, CD10 etc.
- **Unit**: The units of all the corresponding measurements. All units shall follow the units given in Section 5.3 for the corresponding parameter.
- **Height**: Height of the corresponding measurement in m (only number) above/below MSL. For currents, sea temperature etc the depth below mean sea level shall be given with sign ‘-‘.
- **Base**: Key from the database with standardized parameter names (see <https://atmos.app.radix.equinor.com/config/parameters>)
- **Instrument**: Instrument type used to measure given parameter at given height. If given parameter is the merge of measurements from several instrument types, please, list them with comma separator. If there are no instruments available, use NA. Instrument types shall be chosen from the list in Section 5.4.
- **InstrSpec**: Instrument specifications for given quantity. Instrument specifications shall be listed in the same order as the corresponding instrument types.

First 5 rows of the table shall contain time quantities, where only the columns Parameters and Abbrev are filled. Time quantities shall be represented as Year, Month, Day, Hour, Minute in Parameters with corresponding abbreviations YY, MM, DD, HH and Min in Abbrev column.

## Data

The measured data shall be provided in columns below the metadata. In the first row of the data section the column names shall be given. The number of columns with data shall be the same as the number of parameters listed in Parameter Related Metadata section. The first 5 columns shall provide the time as YY (year), MM (month), DD (day), HH (hour), Min (minute). The following columns shall be given names corresponding to the Abbrev name from the header. All parameters shall be in the units specified in the header. Missing values shall be represented by the value given in the header line Missing data.
