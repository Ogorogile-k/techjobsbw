// ============================================================
// ALL JOBS SEARCH
// ============================================================

const searchBar =
    document.getElementById("searchBar");

const locationFilter =
    document.getElementById("locationFilter");

const jobContainer =
    document.getElementById("jobContainer");


// Only run job filtering if the elements exist

if(searchBar && locationFilter && jobContainer){

    searchBar.addEventListener(
        "keyup",
        filterJobs
    );


    locationFilter.addEventListener(
        "change",
        filterJobs
    );


    function filterJobs(){

        let keyword =
            searchBar.value
                .toLowerCase();


        let location =
            locationFilter.value
                .toLowerCase();


        let jobs =
            document.querySelectorAll(
                "#jobContainer .job-card"
            );


        jobs.forEach(job => {

            let title =
                job.querySelector(
                    ".job-title"
                )
                .textContent
                .toLowerCase();


            let jobLocationElement =
                job.querySelector(
                    ".location"
                );


            let jobLocation =
                jobLocationElement
                    ? jobLocationElement.textContent.toLowerCase()
                    : job.textContent.toLowerCase();


            let matchesTitle =
                title.includes(keyword);


            let matchesLocation =
                location === "" ||
                jobLocation.includes(location);


            if(matchesTitle && matchesLocation){

                job.style.display = "block";

            }

            else{

                job.style.display = "none";

            }

        });

    }

}


// ============================================================
// COMPANY SEARCH
// ============================================================

const companySearchBar =
    document.getElementById(
        "companySearchBar"
    );


const companyContainer =
    document.getElementById(
        "companyContainer"
    );


// Only run company filtering if the elements exist

if(companySearchBar && companyContainer){

    companySearchBar.addEventListener(
        "keyup",
        filterCompanies
    );


    function filterCompanies(){

        let keyword =
            companySearchBar.value
                .toLowerCase()
                .trim();


        let companies =
            document.querySelectorAll(
                "#companyContainer .company-card"
            );


        companies.forEach(company => {

            let companyName =
                company.querySelector(
                    ".company-name"
                )
                .textContent
                .toLowerCase();


            if(companyName.includes(keyword)){

                company.style.display = "block";

            }

            else{

                company.style.display = "none";

            }

        });

    }

}