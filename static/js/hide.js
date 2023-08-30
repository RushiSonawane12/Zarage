<!--function yesnoCheck(that) 
{
    if (that.value == "aadhar") 
    {
        document.getElementById("adc").style.display = "block";
    }
    else
    {
        document.getElementById("adc").style.display = "none";
    }
    if (that.value == "pan")
    {
        document.getElementById("pc").style.display = "block";
    }
    else
    {
        document.getElementById("pc").style.display = "none";
    }
    if (that.value == "pass")
    {
       document.getElementById("adc").style.display = "block";
       document.getElementById("pc").style.display = "block";
    }
    else
    {
        document.getElementById("adc").style.display = "none";
        document.getElementById("pc").style.display = "none";
    }
}
<div>
    <select id="selector"  name="deliverytype" onchange="yesnoCheck(this);">
        <option value="select">__Select__</option>
        <option value="aadhar">pickup</option>
        <option value="pan">drop</option>
        <option value="pass">both</option>
    </select> 
  </div>

  <div id="adc" style="display: none;">
    <label for="aadhar">Enter pickup</label> 
    <input type="text" id="aadhar" name="pickup" /><br />
  </div>

<div id="pc" style="display: none;">
    <label for="pan">Enter drop</label> 
    <input type="text" id="pan" name="dropaddress" /><br />
</div>
</div>