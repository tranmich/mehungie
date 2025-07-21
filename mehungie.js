(function () {
  const result = id => document.getElementById(id);
  function fetchRecipe(lat,lng,dish){
    fetch("https://mehungie.onrender.com/clone-dish",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({lat,lng,dish})
    })
    .then(r=>r.json())
    .then(data=>{
       result('mh-result').textContent =
         JSON.stringify(data,null,2);
    })
    .catch(err=>alert("Error: "+err));
  }

  window.addEventListener('DOMContentLoaded',() => {
    const btn = result('mh-go');
    btn.addEventListener('click', () => {
      const dish = result('mh-dish').value || 'burger';
      navigator.geolocation.getCurrentPosition(
        pos => fetchRecipe(pos.coords.latitude,pos.coords.longitude,dish),
        ()  => fetchRecipe(null,null,dish)
      );
    });
  });
})();
