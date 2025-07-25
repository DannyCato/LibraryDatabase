
# Detailing Potential Future Ideas

---

> ## Popularity Tiers
>
> ### Plan
>
> Modify and Add columns into tables to transplant the popularity system into the books so that they can be static on the database and allow for minimal revamping of methods 
>
> ### Hurdles
> 
> - Refactoring to allow for changed due dates and fees
> - - calculate_return_fees 
> - - calculate_days_late
> - - etc.
> - Additional columns in several tables or a new table
> - - extra rows to books table to allow quick access to associated popularity tier. Updated once daily perhaps
> - - added rows in history to show popularity tier at time of checkout
> - - add row to inventory for how many times an individual book has been checked out
> - Hardcoded table for popularity tiers and how they get effected by the library
> 
> #### Difficulty: 6/10
>
> ### Potential Features
>
> - Incentive to return book
> - Potential to search for popular reads
> - Offload librarian work to sql systems for knowledge on popularbooks

> ## Overdue Warnings
>
> ### Plan
>
> Use the contact information to connect with users that have less than half their time with their respective books still available so that people do not hoard certain books. Send email once a day, and when too late send automated calls
>
> ### Hurdles
>
> - Figuring out how to send information and through what applications
> - If an overdue warning is in place then is it right to fine them for being late without reminder?
>
> #### Difficulty: 3/10
>
> ### Potential Features
>
> - Gives librarians a greater opportunity to get their books back since people will eventually check their messages
> - Can't say that we did not remind them
> - Creates additional opportunity for contact