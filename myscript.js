function increment(qty_id)

{
    qty_txt = document.getElementById(qty_id);
    val = parseInt(qty_txt.value);
    if(val<5)
    {
        val += 1;
    }    
    qty_txt.value = val;
}

function decrement(qty_id)

{
    qty_txt = document.getElementById(qty_id);
    val = parseInt(qty_txt.value);
    if(val>1)
    {
        val -= 1;
    }    
    qty_txt.value = val;
}    