--Use capstone database

use capstoneGroup2Database

--Tables for Capstone Data

create table Indicator(
    IndicatorID int primary key identity(1,1),
    IndicatorLabel nvarchar(50) not null
);

create table [Group](
    GroupID int primary key identity(1,1),
    GroupLabel nvarchar(50) not null
)

create table Age(
    AgeID int primary key identity(1,1),
    AgeLabel nvarchar(25) not null
)

create table Sex(
    SexID int primary key identity(1,1),
    SexLabel nvarchar(25) not null
)

create table Race(
    RaceID int primary key identity(1,1),
    RaceLabel nvarchar(50) not null
)

create table Education(
    EducationID int primary key identity(1,1),
    EducationLabel nvarchar(50) not null
)

create table [State](
    StateID int primary key identity(1,1),
    StateLabel nvarchar(25) not null
)

create table Week(
    WeekID int primary key identity(1,1),
    WeekLabel nvarchar(25) not null
)


create table InsuranceCoverage(
    DataID int primary key identity(1,1),
    DataValue decimal(15,3) null,
    IndicatorID int null,
    GroupID int null,
    AgeID int null,
    SexID int null,
    RaceID int null,
    EducationID int null,
    StateID int null,
    WeekID int null,
    constraint fk_InsuranceCoverage_IndicatorID
        foreign key(IndicatorID)
        references Indicator(IndicatorID),
    constraint fk_InsuranceCoverage_GroupID
        foreign key(GroupID)
        references [Group](GroupID),
    constraint fk_InsuranceCoverage_AgeID
        foreign key(AgeID)
        references Age(AgeID),
    constraint fk_InsuranceCoverage_SexID
        foreign key(SexID)
        references Sex(SexID),
    constraint fk_InsuranceCoverage_RaceID
        foreign key(RaceID)
        references Race(RaceID),
    constraint fk_InsuranceCoverage_EducationID
        foreign key(EducationID)
        references Education(EducationID),
    constraint fk_InsuranceCoverage_StateID
        foreign key(StateID)
        references [State](StateID),
    constraint fk_InsuranceCoverage_WeekID
        foreign key(WeekID)
        references Week(WeekID)
)

create table Smoker(
    SmokerID int primary key identity(1,1),
    SmokerLabel bit not null,
)

create table Children(
    ChildrenID int primary key identity(1,1),
    ChildrenLabel nvarchar(25) not null
)

create table Region(
    RegionID int primary key identity(1,1),
    RegionLabel nvarchar(25) not null
)

create table InsuranceCharges(
    ChargeID int primary key identity(1,1),
    ChargeValue decimal (15,3) not null,
    AgeID int not null,
    SexID int not null,
    RegionID int not null,
    SmokerID int not null,
    ChildrenID int not null,
    BMI decimal(15,3) not null,
    constraint fk_InsuranceCharges_AgeID
        foreign key(AgeID)
        references Age(AgeID),
    constraint fk_InsuranceCharges_SexID
        foreign key(SexID)
        references Sex(SexID),
    constraint fk_InsuranceCharges_SmokerID
        foreign key(SmokerID)
        references Smoker(SmokerID),
    constraint fk_InsuranceCharges_ChildrenID
        foreign key(ChildrenID)
        references Children(ChildrenID),
    constraint fk_InsuranceCharges_RegionID
        foreign key(RegionID)
        references Region(RegionID)
)

create table Geocat(
    GeoID int primary key identity(1,1),
    GeoCategory nvarchar(50) not null
)

create table County(
    CountyID int primary key identity(1,1),
    CountyLabel nvarchar(50) null
)

create table Income(
    IncomeID int primary key identity(1,1),
    IncomeLabel nvarchar(50) not NULL
)

create table SAHIE(
    SAHIEID int primary key identity(1,1),
    [Percent_of_Demographic_Uninsured_by_Income_Category] decimal(10,3) not null,
    [Percent_of_Demographic_Insured_by_Income_Category] decimal(10,3) not null,
    [Total_Percent_of_Demographic_Uninsured] decimal(10,3) not null,
    [Total_Percent_of_Demographic_Insured] decimal(10,3) not null,
    AgeID int not null,
    SexID int not null,
    RaceID int not null,
    StateID int not null,
    GeoID int not null,
    CountyID int null,
    IncomeID int not null,
    constraint fk_SAHIE_AgeID
        foreign key(AgeID)
        references Age(AgeID),
    constraint fk_SAHIE_SexID
        foreign key(SexID)
        references Sex(SexID),
    constraint fk_SAHIE_RaceID
        foreign key(RaceID)
        references Race(RaceID),
    constraint fk_SAHIE_StateID
        foreign key(StateID)
        references [State](StateID),
    constraint fk_SAHIE_GeoID
        foreign key(GeoID)
        references Geocat(GeoID),
    constraint fk_SAHIE_CountyID
        foreign key(CountyID)
        references County(CountyID),
    constraint fk_SAHIE_IncomeID
        foreign key(IncomeID)
        references Income(IncomeID)
)

drop table Region;
drop table Indicator;
drop table Age;
drop table Children;
drop table Education;
drop table [Group];
drop table Race;
drop table Sex;
drop table Smoker;
drop table [State];
drop table Week;
drop table Geocat;
drop table County;
drop table Income;

drop table InsuranceCharges;
drop table InsuranceCoverage;
drop table SAHIE;

