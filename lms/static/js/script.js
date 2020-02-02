
/**
 * Called when a page has loaded and wants to apply the active class to the desired menu item.
 * Removes the active class from any other menu item.
 *
 * This function presumes that the list object (ol or ul) wrapping the menu items has an id of menuList
 *
 * As this function uses dom manipluation it is up to the user to check if the DOM content has loaded before using it.
 *
 * @param elementId - Id of the menu item to apply active to
 */
function selectActiveMenuItem(elementId, className) {
    let list = document.querySelectorAll('#menuList > li');

    list.forEach(function (currentLink) {
        if (currentLink.id == elementId) {
            currentLink.classList.add(className);
        }
        else {
            currentLink.classList.remove(className);
        }
    });
}
