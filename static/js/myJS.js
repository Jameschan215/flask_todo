function displayNewTitle()
    {
        let selector =document.getElementById("title-select").selectedIndex;
        let newTitle = document.getElementById("new-title")

        if (selector == 0)
        {
            newTitle.style.display = 'inline';

        }else{
            newTitle.style.display = 'none';
        }
    }