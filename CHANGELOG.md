# Changelog
All notable changes to this project will be documented in this file.

## [0.4.2] - 2020-11-29

- Properly initialize Datepicker (#12 @squio)
- Use previous date-range for initialization if it exists 


## [0.4.1] - 2020-11-26

- Bring back calculateTotalOnObjectArray (#11)
- Bypassing default ordering by when generating the report (#10) 
- Fix in dates in template and view 


## [0.4.0] - 2020-11-24 [BREAKING]

- Renamed `SampleReportView` to `SlickReportView`
- Renamed `BaseReportField` to `SlickReportField`
- Added `SlickReportViewBase` leaving sanity checks for the `SlickReportView`

## [0.3.0] - 2020-11-23

- Add Sanity checks against incorrect entries in columns or date_field
- Add support to create ReportField on the fly in all report types
- Enhance exception verbosity.  
- Removed `doc_date` field reference .

## [0.2.9] - 2020-10-22
### Updated
- Fixed an issue getting a db field verbose column name
- Fixed an issue with the report demo page's filter button not working correctly.

## [0.2.8] - 2020-10-05
### Updated
- Fixed an error with ManyToOne Relation not being able to get its verbose name (@mswastik)


## [0.2.7] - 2020-07-24
### Updates
- Bring back crosstab capability
- Rename `quan` to the more verbose `quantity` 
- Minor enhancements around templates 

## [0.2.6] - 2020-06-06
### Added

- Adds `is_summable` option for ReportFields, and pass it to response
- Add option to override a report fields while registering it.
- Test ajax Request

### Updates and fixes
- Fix a bug with time series adding one extra period. 
- Fix a bug with Crosstab data not passed to `report_form_factory`
- Enhance Time series default column verbose name
- testing: brought back ReportField after unregister test
- Fix Pypi package not including statics.  


## [0.2.5] - 2020-06-04
### Added

- Crosstab support 
- Chart title defaults to report_title
- Enhance fields naming

## [0.2.4] - 2020-05-27
### Added
- Fix a naming issue with license (@iLoveTux)

## [0.2.3] - 2020-05-13
### Added
- Ability to create a ReportField on the fly.
- Document SLICK_REPORTING_DEFAULT_START_DATE & SLICK_REPORTING_DEFAULT_START_DATE settings
- Test Report Field Registry
- Lift the assumption that a Report field name should start and end with "__". This is only a convention now.

 
## [0.2.2] - 2020-04-26
- Port Charting from [Ra Framework](https://github.com/ra-systems/RA)
- Enhance ReportView HTML response


## [0.0.1] - 2020-04-24
### Added
- Ported from [Ra Framework](https://github.com/ra-systems/RA) 
