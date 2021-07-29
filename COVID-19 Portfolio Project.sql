-- Quick glance at the tables

select *
from PortfolioProject..CovidDeaths
order by 3,4

select *
from PortfolioProject..CovidVaccinations
order by 3,4


-- Select data that going to be used

select location, date, total_cases, new_cases, total_deaths, population
from PortfolioProject..CovidDeaths
order by 1,2


-- Shows Likelihood of dying if contract Covid-19

select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
from PortfolioProject..CovidDeaths
--where location like 'Indonesia'
order by 1,2


-- Shows what percentage of population contract Covid-19

select location, date, total_cases, population, (total_cases/population)*100 as PopulationInfectedPercentage
from PortfolioProject..CovidDeaths
--where location like 'Indonesia'
order by 1,2


-- Shows Country with Highest Infection Rate compared to Population

select location, population, MAX(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as PercentagePopulationInfected
from PortfolioProject..CovidDeaths
group by location, population
order by PercentagePopulationInfected desc


-- Shows Country with Highest Death count

select location, MAX(cast(total_deaths as int)) as TotalDeathCount
from PortfolioProject..CovidDeaths
where continent is not null
group by location
order by TotalDeathCount desc


-- Shows Continent with Highest Death count

select location, MAX(cast(total_deaths as int)) as TotalDeathCount
from PortfolioProject..CovidDeaths
where continent is null
group by location
order by TotalDeathCount desc

select continent, MAX(cast(total_deaths as int)) as TotalDeathCount
from PortfolioProject..CovidDeaths
-- where continent is null
group by continent
order by TotalDeathCount desc

-- Global Numbers

select date, SUM(new_cases) as TotalCases, SUM(CAST(new_deaths as int)) as TotalDeaths, SUM(CAST(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
from PortfolioProject..CovidDeaths
where continent is not null
group by date
order by 1

select SUM(new_cases) as TotalCases, SUM(CAST(new_deaths as int)) as TotalDeaths,SUM(CAST(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
from PortfolioProject..CovidDeaths
where continent is not null
order by 1


--  Join tables
 
 select *
 from PortfolioProject..CovidDeaths dea
 join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date


-- Total Population vs Vaccination

select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.date) as TotalVaccinated
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

-- Use CTE

with deavac (Continent, Location, Date, Population, NewVaccination, TotalVaccinated)
as
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.date) as TotalVaccinated
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
)
select *, (TotalVaccinated/Population)*100 as Vaccinationratio
from deavac

-- Use Temp Table

drop table if exists #PercentPopVac
Create Table #PercentPopVac
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
NewVaccination numeric,
TotalVaccinated numeric
)
insert into #PercentPopVac
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(convert(bigint,vac.new_vaccinations)) over (partition by dea.location order by dea.date) as TotalVaccinated
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
--where dea.continent is not null

select *, (TotalVaccinated/Population)*100 as Vaccinationratio
from #PercentPopVac
order by 2,3

-- Creating View to store data for visualization

create view PercentPopulationVaccinated as
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(convert(bigint,vac.new_vaccinations)) over (partition by dea.location order by dea.date) as TotalVaccinated
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null