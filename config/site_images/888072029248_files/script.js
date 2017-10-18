function setCookie (name, value, expires, path, domain, secure) {
	document.cookie = name + "=" + escape(value) +
        ((expires) ? "; expires=" + expires : "") +
        ((path) ? "; path=" + path : "") +
        ((domain) ? "; domain=" + domain : "") +
        ((secure) ? "; secure" : "");
}
function getCookie(name){
	var cookie = " " + document.cookie;
	var search = " " + name + "=";
	var setStr = null;
	var offset = 0;
	var end = 0;
	if (cookie.length > 0) {
		offset = cookie.indexOf(search);
		if (offset != -1) {
			offset += search.length;
			end = cookie.indexOf(";", offset)
			if (end == -1) {
				end = cookie.length;
			}
			setStr = unescape(cookie.substring(offset, end));
		}
	}
	return(setStr);	
}
function authorized(){
	
 	var cookies=document.cookie;
  	var start = cookies.indexOf("ss_reg_" + serialNumber + "=");
  	
  	var signed_in = -1;

  	if (start != -1) {
    	start = cookies.indexOf("=", start) +1;
    	var end = cookies.indexOf("|", start);
    	if (end != -1) {
      		signed_in = cookies.indexOf("|yes", start);
    	}
  	}
  	if (signed_in == -1) {
    	return false;
  	}else{
		return true;  	
	}
}
function showCart(id, pattern){
/**
	Example: 
	pattern = '<span class="price">{price}</span> <span class="items"><strong>{items}</strongs> {itemstext}</span>'
*/
	
	var cartvalues = getCookie("ss_cart_" + serialNumber);
	
	var price = "$0.00";
	var count = 0;
	

	if (cartvalues){
		var values = cartvalues.split("|");

		//Get number of items
		count = values[2].substring(values[2].indexOf(":") + 1)
		
		//Get price		
		price = values[3].substring(values[3].indexOf(":") + 1)
	}
  
	pattern = pattern.replace("{price}", price).replace("{items}", count)
	if(count == 1){
		pattern = pattern.replace("{itemstext}", "item")
	}else{
		pattern = pattern.replace("{itemstext}", "items")
	}
	document.getElementById(id).innerHTML = pattern;  
}
/* end showCart() */

function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

function getSavingHtml(price, newPrice){
	
	price = parseFloat( price.replace(/[ $,]/g, '') )
	
	newPrice = parseFloat( newPrice.replace(/[ $,]/g, '') )
		
	var savingAmount = price - newPrice;
	var savingPersentage = Math.round( (price - newPrice) / price * 100 );
		
	return '<span class="saving">Save $' + numberWithCommas(savingAmount.toFixed(2)) + '  (' + savingPersentage + '%)</span>';
}

// JavaScript Document

$(document).ready(function(){
	$("div.index > span").on("mousemove", function(event){
		if( $("#indexhint").size() == 0 ){
			$("body").append('<div id="indexhint">No results are currently available in this category.</div>')
		}
		var top = event.pageY + 15;
		var left = event.pageX - 40;
		$("#indexhint").css("top", top + "px").css("left", left + "px").show()
	}).on("mouseout", function(){
		$("#indexhint").hide();
	})
	
	$("div.popup").popup();
	$("div.popup span.close").click(function(){
		$(this).closest("div.popup").popup("hide")
	})
	
	//$("#upsell").popup("show")
	$("#upsell .continueshopping").click(function(){
		$("#upsell").popup("hide")
	})
	
	$(".product-info form").submit(function(){

		if( $("#menu_1").size() == 0 ){
			var success = true;
			$(this).find("select").each(function(){
				if( $(this).val().indexOf(";n") > 0){
					success = false;
				}
			})
			if(success == false){
				alert('The product you are trying to purchase requires a menu selection before adding it to the cart. Please make your selection and then add it to the basket.')
				return false;
			}
		}
		
		var success = true;
		$("#product select").each(function(){
			if( $(this).val().indexOf(";n") >= 0 ){
				success = false;
			}
		})
		if(success == false){
			return false;
		}
		
		if($("#upsell").size() == 0){
			return true;
		}		
		
		$("#upsell #added").addClass("loading");
		
		var src = $("#gallery img").attr("src").replace("ss_size3", "ss_size2");
		if($("#product select").size() == 1){
			var id = $("#product input[name='itemnum']").val();
			var selectIndex = $("#product select option:selected").index();
			if(window["image" + id] && window["image" + id][selectIndex] && window["image" + id][selectIndex] != "none"){
				src = window["image" + id][selectIndex];
			}
		}
		
		$("#upsell #added .img img").attr("src", src );
		var h2 = $(".product-header h1").text();
		$("#product select").each(function(){
			var value = $(this).val();
			if( value.indexOf(";") > 0){
				value = value.substring(0, value.indexOf(";"))
			}
			h2 += "<span>" + value + "</span>";
		})
		$("#upsell #added h2").html( h2 );
		var shipping = $( $(".product-info .ships").html() );
		shipping.find( "span.q" ).remove();
		if($(".product-info .ships").hasClass("outofstock") ){
			$("#upsell #added span.ships").addClass("outofstock")
		}else{
			$("#upsell #added span.ships").removeClass("outofstock")
		}
		
		$("#upsell #added span.ships").text( shipping.text() );
		$("#upsell #added div.price").html( $(".product-info .price").html() );
		$("#upsell").popup("show");
		
		$("#upsell #upsell-products h2").text("Customers Who Shopped for " + $(".product-header h1").text() + " Also Shopped For:");
		$("#upsell #upsell-products ul").remove();
		$("#upsell #upsell-products").addClass("loading");
		
		$.ajax({
			type: $(this).attr("method"),
			url: $(this).attr("action"),
			data: $(this).serialize(),
			success: function(msg){
				$("#upsell #added").removeClass("loading");
				showCart("cart", 'Checkout {items} {itemstext}');
			},
			error: function(){
				$("#upsell #added").removeClass("loading");
			}
		});	
		$.ajax({
			type: "get",
			url: "adm/proxy.php",
			data: "sku=" + $("#sku").text(),
			success: function(msg){
				$("#upsell #upsell-products").removeClass("loading");
				var ul = "<ul>";
				var obj = $( msg )
				
				obj.find("results result").each(function(){					
					ul += '<li><a href="' + $(this).find("url").text() + '"><img src="' + $(this).find("image").text() + '" alt="" /></a></li>';
				})
				ul += "</ul>"
				$("#upsell #upsell-products").append( ul );
			},
			error: function(){
				$("#upsell #upsell-products").removeClass("loading");
			}
		});	
		
		return false;
	})
	
	$("#category-products > ul > li > a.buynow").click(function(e){
			
		var success = true;
		
		$(this).closest("li").children("form").find("select").each(function(){
			if($(this).val().indexOf(";n") > 0){
				success = false;
			}
		})
		
		if( success == false ){
			alert( "The product you are trying to purchase requires a menu selection before adding it to the cart. Please make your selection and then add it to the basket." );
			e.preventDefault();
			return false;
		}
		
		if( $("#upsell").size() == 0 ){
			$("body").append(
				'<div id="upsell" class="popup"><span class="close">x</span><div id="added"><h3>Added to Cart</h3><div class="img">' 
					+ '<img src="media/images/pro_comingsoon.gif" alt="" /></div>'
					+ '<div class="info"><h2></h2><span class="ships"></span><div class="price"></div></div>'
					+ '<div class="buttons"><span class="continueshopping">Continue shopping</span><a href="' + baseCgiUrl + '/order.cgi?storeid=' + storeId + '&function=show" class="viewcart">View Cart</a></div></div><div id="upsell-products"><h2></h2></div></div>'
			)
			$("#upsell .close, #upsell .continueshopping").click(function(e){
				$("#upsell").popup("hide");
				e.preventDefault();
				return false;
			})
			$("#upsell").popup();
		}
				
		
		$("#upsell #added").addClass("loading");
		
		var src = $(this).closest("li").find("h2 span.img img").attr("src").replace("ss_size3", "ss_size2");
/*		
		if($("#product select").size() == 1){
			var id = $("#product input[name='itemnum']").val();
			var selectIndex = $("#product select option:selected").index();
			if(window["image" + id] && window["image" + id][selectIndex]){
				src = window["image" + id][selectIndex];
			}
		}
*/
		$("#upsell #added .img img").attr("src", src );
		var h2 = $(this).closest("li").find("h2 span.name").text();
		
		$(this).closest("li").children("form").find("select").each(function(){
			var value = $(this).val();
			if( value.indexOf(";") > 0){
				value = value.substring(0, value.indexOf(";"))
			}
			h2 += "<span>" + value + "</span>";
		})
		
		$("#upsell #added h2").html( h2 );
/*
		var shipping = $( $(".product-info .ships").html() );
		shipping.find( "span.q" ).remove();
		
		$("#upsell #added span.ships").text( shipping.text() );
*/		
		if( $(this).closest("li").find(".statusmessage").hasClass("outofstock") ){
			$("#upsell #added span.ships").addClass("outofstock")
		}else{
			$("#upsell #added span.ships").removeClass("outofstock")
		}

		$("#upsell #added span.ships").text( $(this).closest("li").find(".statusmessage").html() );
		$("#upsell #added div.price").html( $(this).closest("li").find(".price").html() );
		
		$("#upsell").popup("show");
		
		$("#upsell #upsell-products h2").text("Customers Who Shopped for " + $(this).closest("li").find("h2 span.name").text() + " Also Shopped For:");
		$("#upsell #upsell-products ul").remove();
		$("#upsell #upsell-products").addClass("loading");
		
		var sku = $(this).closest("li").find(".sku").text();
		
		
		if( $(this).closest("li").children("form").size() > 0){//need to send form with drop down
			$.ajax({
				type: "post",
				url: $(this).closest("li").children("form").attr("action"),
				data: $(this).closest("li").children("form").serialize(),
				success: function(msg){
					$("#upsell #added").removeClass("loading");
					showCart("cart", 'Checkout {items} {itemstext}');
				},
				error: function(){
					$("#upsell #added").removeClass("loading");
					//alert("Something wrong. Please try again later.")
				}
			});	
			
		}else{
			$.ajax({
				type: "get",
				url: $(this).attr("href"),
				success: function(msg){
					$("#upsell #added").removeClass("loading");
					showCart("cart", 'Checkout {items} {itemstext}');
				},
				error: function(){
					$("#upsell #added").removeClass("loading");
					//alert("Something wrong. Please try again later.")
				}
			});	
		}
		$.ajax({
			type: "get",
			url: "adm/proxy.php",
			data: "sku=" + sku,
			success: function(msg){
				$("#upsell #upsell-products").removeClass("loading");
				var ul = "<ul>";
				var obj = $( msg )
				
				obj.find("results result").each(function(){					
					ul += '<li><a href="' + $(this).find("url").text() + '"><img src="' + $(this).find("image").text() + '" alt="" /></a></li>';
				})
				ul += "</ul>"
				$("#upsell #upsell-products").append( ul );
			},
			error: function(){
				$("#upsell #upsell-products").removeClass("loading");
			}
		});			
				
		e.preventDefault();
		return false;
	})
	
	if( $("a.menu-link:visible").size() == 0 ){
		$("#freeshipping").click(function(e){
			$("#freeshippingpopup").popup("show")
			e.preventDefault();
			return false;
		})
	}
	
	if( $("#bannerpopup").size() > 0 ){
		$("article.content > div.banner, #category-content > div.banner").click(function(e){
			if($("#bannerpopup").size() > 0){
				$("#bannerpopup").popup("show")
				e.preventDefault();
				return false;
			}
			return true;
		})
	}
	
	$("#nocoupon").click(function(){
		$("#nocouponpoup").popup("show")
	})
	$("#applycode").click(function(){
		$("#nocouponpoup").popup("hide")
		var code = $(this).closest("h2").find("strong").text();
		$("input[name='coupon_code']").val( code )
		$(".coupons input[type='submit']").click();
	})
	
	
	//setCookie("promotion", "", "Thu, 01-Jan-1970 00:00:01 GMT");
	var promotion = getCookie("promotion");
	if(promotion == null && $("#getonthelist form").size() > 0 && $("a.menu-link:visible").size() == 0){//show only for desktop devices
		
		$("#getonthelist form").validate({submitHandler: function(){
			//<strong>Thank you!</strong><br />
			//A welcome message has been sent to your email address.
			var today = new Date();
			today.setTime( today.getTime() );
			var expires_date = new Date( today.getTime() + (60*60*24*365*1000) );
			setCookie("promotion", 1, expires_date.toGMTString());
			this.submit();
			return true;
		}});
		$("#getonthelist").popup({
			onclose: function(){
				var today = new Date();
				today.setTime( today.getTime() );
				var expires_date = new Date( today.getTime() + (60*60*24*365*1000) );
				setCookie("promotion", 1, expires_date.toGMTString());
			}
		});
		$("#getonthelist span.close, #getonthelist .nothanks").click(function(){
			var today = new Date();
			today.setTime( today.getTime() );
			var expires_date = new Date( today.getTime() + (60*60*24*365*1000) );
			setCookie("promotion", 1, expires_date.toGMTString());
			$("#getonthelist").popup("hide");
		})
	
		$("#getonthelist").popup("show");
		
	}

	$("#product > #recently-viewed").click(function(){
		if( $(this).hasClass("active") ){
			if( $("a.menu-link:visible").size() > 0 ){
				$(this).removeClass("active")
			}
		}else{
			$(this).addClass("active")
		}
	})
	$("#product > #recently-viewed .close").click(function(e){
		$("#product > #recently-viewed").removeClass("active")
		e.preventDefault();
		return false;
	})
	
	
	$("#newsletter form").validate();
	
	$(".subnav").closest("li").mouseover(function(){
		$(this).addClass("active");
	}).mouseleave(function(){
		$(this).removeClass("active");
	})
	
	
	$("body > footer nav h3").click(function(){
		if( $(this).hasClass("active") ){
			$(this).removeClass("active")
		}else{
			$(this).addClass("active")			
		}
	})
	
//site navigation	
	$("a.menu-link").click(function(){
		if( $(this).hasClass("active") ){
			$(this).removeClass("active")
		}else{
			$(this).addClass("active");
		}
	})
	
	$("header nav > ul > li > span, header nav > ul > li > a.h3").click(function(event){
		if( $("a.menu-link:visible").size() > 0 ){
			if( $(this).hasClass("active") ){
				$(this).removeClass("active")
			}else{
				$(this).addClass("active")
			}
			event.preventDefault();
		}
	})
	
	$("header nav h3").click(function(event){
		if( $("a.menu-link:visible").size() > 0 ){
			if( $(this).hasClass("active") ){
				$(this).removeClass("active")
			}else{
				$(this).addClass("active")
			}
			event.preventDefault();
		}
	})	
	
//Fixing height of content
	function fixHeight(){
		var footerHeight = $("body > footer").height() + parseFloat( $("body > footer").css("paddingTop") ) + parseFloat( $("body > footer").css("paddingBottom") );
		var headerHeight = $("body > header").height() + parseFloat( $("body > header").css("paddingTop") ) + parseFloat( $("body > header").css("paddingBottom") );
	
		var height = $(window).height() - footerHeight - headerHeight - parseFloat( $("body > article.content").css("paddingTop") ) - parseFloat( $("body > article.content").css("paddingBottom") );
		$("body > article.content").css("minHeight", height + "px");
	}
	fixHeight();
	$(window).resize(fixHeight);
	
	$( window ).scroll(function() {
		if ( $(this).scrollTop() > 80 ) {
			$("body").addClass("scroll")
		}else{
			$("body").removeClass("scroll")
		}
		
	});	
	
try{
	$("a.livechat").click(function(event){
		$("div#livechat div").trigger("click");
		event.preventDefault();
	});
}catch(e){}
	
		
//Home page slider
(function(){
	var maxHeight = 0;
	var maxH2Height = 0;
	$("#homeslider li").each(function(){
		maxHeight = Math.max(maxHeight, $(this).height());
		maxH2Height = Math.max(maxH2Height, $(this).find("h2").height());
	})
	
	$("#homeslider li").each(function(){
		$(this).css("minHeight", maxHeight + "px");
		$(this).find("h2").css("minHeight", maxH2Height + "px");
	})
	$("#homeslider div.info").css("maxHeight", (maxHeight + 100) + "px");
	$("#homeslider div.info .desc").css("minHeight", (maxHeight + 90) + "px");
})();

$(window).resize(function(){
	$("#homeslider ul").css("width", (225 + 20)*$("#homeslider ul li:visible").size() + "px");
})
$("#homeslider ul").css("width", (225 + 20)*$("#homeslider ul li:visible").size() + "px");

if( $(".menu-link:visible").size() == 0){
	$("#homeslider").jScrollPane({animateScroll: true});
}


if( $("#homeslider").size() > 0 ){
	//we need to reinitialize jScrollPane on window resize
	$(window).resize(function(){
		if( $(".menu-link:visible").size() == 0){
			$("#homeslider").jScrollPane({reinitialise: true, animateScroll: true});
		}else{//we need to remove jScrollPage
			$("#homeslider").data('jsp').destroy();	
		}
	})
	
	var stopAutoScrolling = false;
	var lastPanePosition = 0;
	setInterval(function(){
		if(stopAutoScrolling == false){
			var api = $("#homeslider").data('jsp');	
			if(api){
				var newPanePosition = api.getContentPositionX();
				var width = api.getContentWidth();
		
				if(lastPanePosition == newPanePosition){
					if( $(".menu-link:visible").size() == 0){
						var offset = 4 * (225 + 19);
					}else{
						var offset = 2 * (225 + 19);
					}
					api.scrollByX(offset, true);
					lastPanePosition += offset;
				}else if(width - newPanePosition == $("article.content").width()){
					api.scrollToX(0, true);
					lastPanePosition = 0;
				}else{
					lastPanePosition = newPanePosition;
				}
			}
		}
	}, 7000);
}
$("#homeslider h2 img").mouseenter(function(event){
	if( $(".menu-link:visible").size() == 0){
		stopAutoScrolling = true;
		
		var api = $("#homeslider").data('jsp');	
		var newPanePosition = api.getContentPositionX();
		
		if( $(this).closest("li").index() * (225+19) - newPanePosition < 0){
			return;
		}
		if( $(this).closest("li").index() * (225+19) - newPanePosition > 750){
			return;
		}
		
		var parentOffset = $(this).closest("div#homeslider").offset();
		var x = event.pageX - parentOffset.left;		
		if(x > $(this).closest("div#homeslider").width() / 2){
			$(this).closest("li").addClass("right");
		}
	
		$(this).closest("li").addClass("active");
		$(this).closest("li").find("div.info .desc").jScrollPane();
	}
}).closest("li").mouseleave(function(){
	stopAutoScrolling = false;
	$(this).removeClass("active").removeClass("right")
})
$("#homeslider div.info .close").click(function(){
	$(this).closest("li").removeClass("active");
})






$("div.p .readmore").click(function(){
	if( $(this).closest("div.p").hasClass("all") ){
		$(this).closest("div.p").removeClass("all")
	}else{
		$(this).closest("div.p").addClass("all");
	}
})

$("div.p span.read").closest("a").click(function(e){
	e.preventDefault();
	if( $(this).text() == "Read more..." ){
		$(this).find("strong").text("Collapse");
		$(this).closest("div.p").find(".hide-show").show();
	}else{
		$(this).find("strong").text("Read more...");
		$(this).closest("div.p").find(".hide-show").hide();
	}
})


$("body > article.content ul.nav > li > a").click(function(e){
	e.preventDefault();
	if( $(this).closest("li").hasClass("active") ){
		$(this).closest("ul").find("li.active").removeClass("active");
	}else{
		$(this).closest("ul").find("li.active").removeClass("active");
		$(this).closest("li").addClass("active");
	}
})

$('.fancybox').fancybox();
$('.ssd_box_gallery').fancybox({
        prevEffect : 'none',
        nextEffect : 'none',

        autoPlay  : true,
        playSpeed : 6000,
        closeBtn  : false,
        arrows    : true,
        nextClick : false,
        helpers : {
            title : null
        }
});

$("#vinyllink").click(function(){
	
	if( $(".menu-link:visible").size() == 0){
		if( $("#vinylpopup").size() == 0 ){
			var html = '<div id="vinylpopup"><span class="close">x</span>';
			html += $("#vinyl .subnav").html();
			html += "</div>";
		
			$("article.content").append(html);
		
			$("#vinylpopup").popup();
			$("#vinylpopup .close").click(function(){
				$("#vinylpopup").popup("hide");
			});
		}
		$("#vinylpopup").popup("show");
	}else{
		if( $("header > nav:visible").size() == 0){
			$(".menu-link").trigger("click");
		}
		if( $(".subnav").eq(0).closest("li").find(".subnav:visible").size() == 0 ){
			$(".subnav").eq(0).closest("li").find(".h3").trigger("click")
		}
	}
})

$("#equipmentlink").click(function(){
	
	if( $(".menu-link:visible").size() == 0){
		if( $("#equipmentpopup").size() == 0 ){
			var html = '<div id="equipmentpopup"><span class="close">x</span>';
			html += $("#equipment .subnav").html();
			html += "</div>";
		
			$("article.content").append(html);
		
			$("#equipmentpopup").popup();
			$("#equipmentpopup .close").click(function(){
				$("#equipmentpopup").popup("hide");
			});
		}
		$("#equipmentpopup").popup("show");
	}else{
		if( $("header > nav:visible").size() == 0){
			$(".menu-link").trigger("click");
		}
		if( $(".subnav").eq(0).closest("li").find(".subnav:visible").size() == 0 ){
			$(".subnav").eq(0).closest("li").find(".h3").trigger("click")
		}
	}
})

$("#category-mnav li").click(function(){
	if( !$(this).hasClass("active") ){
		$("#category-mnav li").removeClass("active");
		$(this).addClass("active")
		switch( $(this).attr("id") ){
			case "nav-results":
				$("#category-filters").hide();
				$("#category-sorting").hide();
				$("#category-content").show();
			break;
			case "nav-filters":
				$("#category-filters").show();
				$("#category-sorting").hide();
				$("#category-content").hide();
			break;
			case "nav-sorts":
				$("#category-filters").hide();
				$("#category-sorting").show();
				$("#category-content").hide();
			break;
		}
	}
})
$("#category-filters .filters h5").click(function(){
	if( $(this).hasClass("active") ){
		$(this).removeClass("active");
	}else{
		$(this).addClass("active");
	}
})

$("#filters input[type='checkbox']").change(function(){
	document.location.href = $(this).closest("li").find("a").attr("href");
})


/*
$(".product-info form").submit(function(){
	var result = true;
	if( $(".product-info .quantitypricing").size() == 0 ){
		$(".product-info .options select").each(function(index, select){
			var _value = $(select).val();
			if( _value.indexOf(";n") > 0){
				result = false;
			}
		})
	}
	if( result == false ){
		alert("Please choose all options.")
	}
	return false;
})
var defaultPriceHTML = null;
$(".product-info .options select").change(function(){
	
	function _getOptionPrice(basePrice, option){
	}
	
	if( defaultPriceHTML == null){
		defaultPriceHTML = $(".product-info .price").html();
	}
	if( $(".product-info .quantitypricing").size() == 0 && $(".product-info .options select").size() == 1){
		var _value = $(".product-info .options select").val();
		if( _value.indexOf(";n") > 0){
			$(".product-info .price").html( defaultPriceHTML );
		}else{
			var _values = _value.split(";");
			if( _values.length == 0){
				$(".product-info .price").html( defaultPriceHTML );
			}else{
				var _priceHTML = "$" + _getOptionPrice(basePrice, parseFloat( _values[1] )).toFixed(2);
				$(".product-info .price").html( _priceHTML );		
			}
		}
	}
})
*/

	
	//fixing height for product list
	function fixProductsHeight(){
		if( $("#category-products > ul > li, ul.products > li").attr("height") == null){
			$("#category-products > ul > li, ul.products > li").each(function(){
				if( $(this).height() > 0){
					$(this).attr("height", $(this).height() );
				}
			})
		}
		
		$("#category-products > ul > li, ul.products > li").each(function(index, li){
			
			if( $(this).css("clear") == "both" ){
				
				var height = $(this).attr("height");
				var h2Height = $(this).find("h2").height();
				var typeHeight = $(this).find("span.type").height();
				var priceHeight = $(this).find("div.price").height();
				var summaryHeight = $(this).find(".summary").height();
				var statusHeight = $(this).find("span.status").height();
				var outofstock = ($(this).find("a.buynow").size() > 0);
				var currentLi = $(this);
				while(currentLi.next() && currentLi.next().css("clear") == "none"){
					
					height = Math.max(height, currentLi.next().attr("height"));
					h2Height = Math.max(h2Height, currentLi.next().find("h2").height());
					typeHeight = Math.max(typeHeight, currentLi.next().find("span.type").height());
					priceHeight = Math.max(priceHeight, currentLi.next().find("div.price").height());
					summaryHeight = Math.max(summaryHeight, currentLi.next().find(".summary").height());
					statusHeight = Math.max(statusHeight, currentLi.next().find("span.status").height());
					outofstock = outofstock || (currentLi.next().find("a.buynow").size() > 0)
					currentLi = currentLi.next();
				}
				
				var currentLi = $(this);
				currentLi.css("minHeight", height + "px")
				currentLi.find("h2").css("minHeight", h2Height + "px")
				currentLi.find("span.type").css("minHeight", typeHeight + "px")
				currentLi.find("div.price").css("minHeight", priceHeight + "px")
				currentLi.find(".summary").css("minHeight", summaryHeight + "px")
				currentLi.find("span.status").css("minHeight", statusHeight + "px")
				if(outofstock){
					currentLi.removeClass("outofstock")
				}else{
					currentLi.addClass("outofstock")
				}
				while(currentLi.next() && currentLi.next().css("clear") == "none"){
					currentLi.next().css("minHeight", height + "px")
					currentLi.next().find("h2").css("minHeight", h2Height + "px")
					currentLi.next().find("span.type").css("minHeight", typeHeight + "px")
					currentLi.next().find("div.price").css("minHeight", priceHeight + "px")
					currentLi.next().find(".summary").css("minHeight", summaryHeight + "px")
					currentLi.next().find("span.status").css("minHeight", statusHeight + "px")
					if(outofstock){
						currentLi.next().removeClass("outofstock")
					}else{
						currentLi.next().addClass("outofstock")
					}
					currentLi = currentLi.next();
				}
			}
			
			
		})
	}
	fixProductsHeight();
	$(window).resize(fixProductsHeight);
/*	
	$("#category-products select").change(function(){
		var id = $(this).closest("li").attr("id").replace("product_", "");
		$("div#quickview_" + id + " select").val( $(this).val() );
	})
*/	
	$("#category-products select, div.quickview select").change(function(){
		
		var priceHTML = $(this).closest("li,div.quickview").attr("priceHTML");
		if(priceHTML == null){
			priceHTML = $(this).closest("li,div.quickview").find("div.price").html();
			$(this).closest("li,div.quickview").attr("priceHTML", priceHTML);
		}
		
		var modifiedPrice = parseFloat( $(this).closest("li,div.quickview").find("div.price").attr("basePrice") );
		var useDefaultPrice = true;
		
		if( $(this).closest("form").find("input[name='type']").val() == "simple"){
				
			$(this).closest("li,div.quickview").find("select").each(function(){
				if(this.options[this.selectedIndex].value.indexOf(";n") == -1){
					var modifier = this.options[this.selectedIndex].value
				
					if(modifier.indexOf(";") > 0){
						useDefaultPrice = false;
						modifier = modifier.substring(modifier.indexOf(";") + 1)
						if(modifier.indexOf("=") >= 0){
							modifier = modifier.substring(modifier.indexOf("=") + 1)
						}
						modifiedPrice += parseFloat(modifier);//TODO: need to process different modifiers				
					}
				}
			})
		
		}else{//advanced ordering options
			
			if( $(this).closest("form").find("select").size() == 2 ){// 2 levels
				
				if( $(this).attr("name").indexOf(":finopt:0") > 0 ){
				
					var options = $(this).closest("form").find("select").eq(0).find("option:selected").attr("options")
					if(options){
						$(this).closest("form").find("select").eq(1).find("option:nth-child(n+2)").remove();
						var options = eval(options);
						for(var i = 0; i < options.length; i++){
							var option = options[i];
						
							var value = option.text;
							if(option.modifier){
								value += ";" + option.modifier
							}
							var html = '<option value="' + value + '">' + option.text + '</option>';
						
							$(this).closest("form").find("select").eq(1).append(html)
						}
						$(this).closest("form").find("select").eq(1).prop("disabled", false);
					
					}else{
						$(this).closest("form").find("select").eq(1).prop("disabled", true);					
					}				
				}else{//updating the second drop down. need to update price if necessary

					if(this.options[this.selectedIndex].value.indexOf(";n") == -1){
						var modifier = this.options[this.selectedIndex].value
				
						if(modifier.indexOf(";") > 0){
							useDefaultPrice = false;
							modifier = modifier.substring(modifier.indexOf(";") + 1)
							if(modifier.indexOf("=") >= 0){
								modifier = modifier.substring(modifier.indexOf("=") + 1)
							}
							modifiedPrice += parseFloat(modifier);//TODO: need to process different modifiers				
						}
					}
				
				}
				
			}else{//1 level only
				if(this.options[this.selectedIndex].value.indexOf(";n") == -1){
					var modifier = this.options[this.selectedIndex].value
				
					if(modifier.indexOf(";") > 0){
						useDefaultPrice = false;
						modifier = modifier.substring(modifier.indexOf(";") + 1)
						if(modifier.indexOf("=") >= 0){
							modifier = modifier.substring(modifier.indexOf("=") + 1)
						}
						modifiedPrice += parseFloat(modifier);//TODO: need to process different modifiers				
					}
				}
			}
		}
		
		if( useDefaultPrice == true ){
			$(this).closest("li,div.quickview").find("div.price").html( priceHTML );
		}else{
			$(this).closest("li,div.quickview").find("div.price").html( "$" + numberWithCommas (modifiedPrice.toFixed(2)) );
		}
		
		
	})
	$("#category-products select").eq(0).change();
/*	
	$("#category-products li > form select").closest("li").children("a.buynow").click(function(e){
		var success = true;
		
		$(this).closest("li").children("form").find("select").each(function(){
			if($(this).val().indexOf(";n") > 0){
				success = false;
			}
		})
		
		if( success == false ){
			alert( "The product you are trying to purchase requires a menu selection before adding it to the cart. Please make your selection and then add it to the basket." );
		}else{
			$(this).closest("li").find("form").submit();
		}
		e.preventDefault();
	})
*/	
	
	$("div.quickview select").closest("div.quickview").find("a.buynow").click(function(e){
		var success = true;
		
		$(this).closest("div.quickview").find("select").each(function(){
			if($(this).val().indexOf(";n") > 0){
				success = false;
			}
		})
		
		if( success == false ){
			alert( "The product you are trying to purchase requires a menu selection before adding it to the cart. Please make your selection and then add it to the basket." );
		}else{
			$(this).closest("div.quickview").find("form").submit();
		}
		e.preventDefault();
	})
	
	
	$("#category-products span.quickview").click(function(e){
		//closeelement
		
		var id = $(this).closest("li").attr("id").replace("product_", "");
		$("#quickview_" + id).popup({closeelement: ".close"}).popup("show");
		//$("#quickview_" + id + " .desc").jScrollPane({reinitialise: true, animateScroll: true});
		e.preventDefault();
	})
	
	$("#product form .qty input[type='text']").keyup(function(){
		if(window.quantities && window.prices){//need to update the price
			var value = parseInt( $(this).val() );
			if(value >= 1){
				var index = 0;
				while(index < quantities.length && quantities[index] <= value){
					index++;
				}
				var newPriceHTML = prices[index-1];
				$("#product .price").html(newPriceHTML)
			}
		}
	})
	
//More information product tabs
$("#product-tabs > ul > li").click(function(){
	$("#product-tabs > ul > li.active").removeClass("active");
	$(this).addClass("active");
	$("#product-tabs > div.active").removeClass("active");
	$("#product-tabs > div").eq( $(this).index() ).addClass("active");
})
	
  	$(".aggregaterating").click(function(event){
		if ( !$("#product-tabs > ul > li#reviews").hasClass('active') ){
			$('#product-tabs > ul > li.active').removeClass('active');
			$("#product-tabs > ul > li#reviews").addClass('active');
				
			$("#product-tabs > div.active").removeClass("active");
			$('#product-tabs > div').eq( $("#product-tabs > ul > li#reviews").index() ).addClass('active');
		}
		return true;
  	})	
	
	
	$(".gallerybox #gallery li").click(function(){
		$(".maingraphicwrapper img").eq(0).attr("src", $(this).find("img").attr("src").replace("ss_size3", "ss_size1"))
		$(".gallerybox #gallery li").removeClass("active");
		$(this).addClass("active");
	})
	

	var cellWidth = 62 + 5;
	var paddingLeft = 23;
		
	if( $(".gallerybox #gallery li").size() * cellWidth > $(".gallerybox").width() ){
		if($(".gallerybox .next, .gallerybox .prev").size() == 0){
			$(".gallerybox").append('<a href="#" class="next"><span>Next</span></a><a href="#" class="prev disabled"><span>Previous</span></a>')			
		}else{
			$(".gallerybox .next, .gallerybox .prev").show();
		}
		$(".gallerybox #gallery").css("left", paddingLeft + "px");
			
		$(".gallerybox .next").click(function(event){
			event.preventDefault();
				
			var left = parseInt($(".gallerybox #gallery").css("left"));
			var max = $(".gallerybox").width() - cellWidth * $(".gallerybox #gallery li").size() - paddingLeft + 8
			left = Math.max(left - cellWidth * 2, max);
				
			$(".gallerybox #gallery").animate({left: left}, 300);
				
			if(left == max){
				$(".gallerybox .next").addClass("disabled")
			}
				
			$(".gallerybox .prev").removeClass("disabled")
		})

		$(".gallerybox .prev").click(function(event){
			event.preventDefault();
				
			var left = parseInt($(".gallerybox #gallery").css("left"));
			left = Math.min(left + cellWidth * 2, paddingLeft);
			$(".gallerybox #gallery").animate({left: left}, 300);
				
			if(left == paddingLeft){
				$(".gallerybox .prev").addClass("disabled")
			}
			$(".gallerybox .next").removeClass("disabled")
		})
	}else{
		$(".gallerybox .next, .gallerybox .prev").hide();
		$(".gallerybox #gallery").css("left","0px");
	}
	
	$(window).resize(function(){
		if( $(".gallerybox #gallery li").size() * cellWidth > $(".gallerybox").width() ){

			if($(".gallerybox .next, .gallerybox .prev").size() == 0){
				$(".gallerybox").append('<a href="#" class="next"><span>Next</span></a><a href="#" class="prev disabled"><span>Previous</span></a>')			
			}else{
				$(".gallerybox .next, .gallerybox .prev").show();
			}
			$(".gallerybox #gallery").css("left", paddingLeft + "px");
			
		}else{
			$(".gallerybox .next, .gallerybox .prev").hide();
			$(".gallerybox #gallery").css("left","0px");			
		}
		
	});
	
	(function initImgs(){
		if( $(".gallerybox li").size() > 0){
			var ul = $(".gallerybox ul").clone()
			ul.find("li:first-child").remove();
			var html = ul.html().replace(/_small/g, "_medium").replace(/ss_size3/g, "ss_size1");
			
			$("#imgs").append(html)
			
		}
	})()

	
	var currentImg = 0;
	var maxImages = $("#imgs li").size();
	var speed = 500;
	
	var imgs = $("#imgs");
		
	if( $("#imgs li").size() > 1){
		$(".maingraphicwrapper").append('<span class="next">&gt;</span><span class="prev disabled">&lt;</span>')
		$(".maingraphicwrapper .next").click(function(){
			nextImage();
		})
		$(".maingraphicwrapper .prev").click(function(){
			previousImage();			
		})
	}
	
	$("#imgs").swipe({
		triggerOnTouchEnd: true,
        swipeStatus: swipeStatus,
        allowPageScroll: "vertical",
        threshold: 75
	});
	


        /**
         * Catch each phase of the swipe.
         * move : we drag the div
         * cancel : we animate back to where we were
         * end : we animate to the next image
         */
        function swipeStatus(event, phase, direction, distance) {
			if( $(".menu-link:visible").size() == 0 ){
				return;
			}
			
            //If we are moving before swipe, and we are going L or R in X mode, or U or D in Y mode then drag.
            if (phase == "move" && (direction == "left" || direction == "right")) {
                var duration = 0;

                if (direction == "left") {
                    scrollImages(($("#imgs li").width() * currentImg) + distance, duration);
                } else if (direction == "right") {
                    scrollImages(($("#imgs li").width() * currentImg) - distance, duration);
                }

            } else if (phase == "cancel") {
                scrollImages($("#imgs li").width() * currentImg, speed);
            } else if (phase == "end") {
                if (direction == "right") {
                    previousImage();
                } else if (direction == "left") {
                    nextImage();
                }
            }
        }

        function previousImage() {
            currentImg = Math.max(currentImg - 1, 0);
            scrollImages($("#imgs li").width() * currentImg, speed);
			
			$(".maingraphicwrapper .next").removeClass("disabled");			
			if(currentImg == 0){
				$(".maingraphicwrapper .prev").addClass("disabled");
			}
			$("#gallery li").removeClass("active");
			$("#gallery li").eq(currentImg).addClass("active")
			
        }

        function nextImage() {
            currentImg = Math.min(currentImg + 1, maxImages - 1);
            scrollImages($("#imgs li").width() * currentImg, speed);
			
			$(".maingraphicwrapper .prev").removeClass("disabled");			
			if(currentImg == (maxImages - 1) ){
				$(".maingraphicwrapper .next").addClass("disabled");
			}			
			$("#gallery li").removeClass("active");
			$("#gallery li").eq(currentImg).addClass("active")
        }

        /**
         * Manually update the position of the imgs on drag
         */
        function scrollImages(distance, duration) {
            imgs.css("transition-duration", (duration / 1000).toFixed(1) + "s");

            //inverse the number we set in the css
            var value = (distance < 0 ? "" : "-") + Math.abs(distance).toString();
            imgs.css("transform", "translate(" + value + "px,0)");
        }	
	
	
	

	$('.jcarousel')
		.jcarousel({
			wrap: 'circular',
			vertical: false,
			animation: 400  //The speed of the scroll animation in milliseconds
		})
		.jcarouselAutoscroll({
			interval: 5000 //The autoscrolling interval in milliseconds
		});
		
	$('.jcarousel-pagination')
		.on('jcarouselpagination:active', 'a', function() {
			$(this).addClass('active');
		})
		.on('jcarouselpagination:inactive', 'a', function() {
			$(this).removeClass('active');
		}).jcarouselPagination();
	
	$(".bslideshow")
		.jcarousel({
			wrap: 'circular',
			vertical: false,
			animation: 400  //The speed of the scroll animation in milliseconds		
		})
		.jcarouselAutoscroll({
			interval: 5000 //The autoscrolling interval in milliseconds
		})
   $('.bslideshow .prev')
            .on('jcarouselcontrol:active', function() {
                $(this).removeClass('inactive');
            })
            .on('jcarouselcontrol:inactive', function() {
                $(this).addClass('inactive');
            })
            .jcarouselControl({
                target: '-=1'
            });		
		
	$('.bslideshow .next')
            .on('jcarouselcontrol:active', function() {
                $(this).removeClass('inactive');
            })
            .on('jcarouselcontrol:inactive', function() {
                $(this).addClass('inactive');
            })
            .jcarouselControl({
                target: '+=1'
            });	

	$(".bslideshow a.coupon").click(function(e){
		if($("#bannerpopup").size() > 0){
			$("#bannerpopup").popup("show")
			e.preventDefault();
			return false;
		}
		return true;
	})
	
	$("#messages").each(function() {
    	if ($.trim($(this).html())){
        	$(this).show();
    	}
	});	
		
	//shopping cart
	if( $("table.cart td.cart_op").size() == 0){
	
		if( $("table.totals td.totals_txt:contains(Gift Cert M)").size() > 1){
			$("table.totals td.totals_txt:contains(Gift Cert M)").last().append("<span class='remove-cert remove-cert-all'>Remove ALL Certificates</span>")
		}else{
			$("table.totals td.totals_txt:contains(Gift Cert M)").append("&nbsp;&nbsp;<span class='remove-cert'>(<strong>X</strong>)</span>")		
		}
	}
	$("table.totals span.remove-cert").click(function(){
		//TODO: check the situation with several Gift Certifications
		/*
			1. Show loading mask
			2. Empty cart
			3. Add all products again to the cart
		*/
		ss_jQuery("form.order").mask( loadmaskphrase );
		
		var form = $("<form method='post' action='" + $("form.order").attr("action") + "'>"
						+ "<input type='hidden' name='function' value='add' />"
						+ "<input type='hidden' name='storeid' value='" + storeId + "' />"
						+ "<input type='hidden' name='dbname' value='products' />"
					+ "</form>")
		$("table.cart td.cart_sku").each(function(){
			//TODO: it is necessary to add products with options
			form.append("<input type='text' name='sku' value='" + $(this).text() + "' />");
			form.append("<input type='text' name='" + $(this).text() + ":qnty' value='" + $(this).closest("tr").find(".cart_quantity input").val() + "' />");
		})
		
		//<input class="button9" name="function" id="Empty Cart" value="Empty Cart" tabindex="1" onclick="return(CheckIt(9,0));" type="submit">
		$("form.order").append('<input type="function" name="function" value="Empty Cart" />')
		
		$.ajax({
				type: $("form.order").attr("method"),
				url: $("form.order").attr("action"),
				data: $("form.order").serialize(),
				success: function(msg){
					form.appendTo('body').submit();
				},
				error: function(){
					form.appendTo('body').submit();
					//alert("We are not able to remove applied gift certificate now. Try again later.")
					//ss_jQuery("form.order").unmask( loadmaskphrase );
				}
			});
	})
	
	
	$(".sccheck input").change(function(){
		if( $(this).prop("checked") ){			
			$("textarea[name='Comments']").val("Please open and pack my records to avoid seamsplits.\n\n" + $("textarea[name='Comments']").val())
		}else{
			$("textarea[name='Comments']").val( $("textarea[name='Comments']").val().replace("Please open and pack my records to avoid seamsplits.\n\n", "").replace("Please open and pack my records to avoid seamsplits.\n", "").replace("Please open and pack my records to avoid seamsplits.", "") )
		}
	})
	
	$("#holidayinfo").popup();
	$("#holidayinfo .close").click(function(){
		$("#holidayinfo").popup("hide");
	})
	$("#holiday").click(function(){
		$("#holidayinfo").popup("show");
	})

	$("#dsspopup").popup();
	$("#dsspopup .close").click(function(){
		$("#dsspopup").popup("hide");
	})
	$("#isspopup").popup();
	$("#isspopup .close").click(function(){
		$("#isspopup").popup("hide");
	})
	$("#dss").click(function(){
		$("#dsspopup").popup("show");
		e.preventDefault();
	})
	$("#iss").click(function(e){
		$("#isspopup").popup("show");
		e.preventDefault();
	})
	
	$(".outofstockform form").validate({
		submitHandler: function(form) {
			$(".outofstockform").addClass("loading");
			$.ajax({
				type: $(form).attr("method"),
				url: $(form).attr("action"),
				data: $(form).serialize(),
				success: function(msg){
					alert(msg); 
					$(".outofstockform").removeClass("loading");
				},
				error: function(){
					//alert("Something wrong. Please try again later.")
					$(".outofstockform").removeClass("loading");
				}
			});
		}
	});
	
$(".maingraphicwrapper img").eq(0).attr("name", "prod_img");

function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}


$("#product div.price").find("script").remove();

if( $("#product select").size() == 1 && window.options){
	
	defaultShippingStatus = $( "#product .ships" ).html();
	defaultShippingOutOfStock = $( "#product .ships" ).hasClass("outofstock");	
	
	function updateShippingStatus(){
		
		if( $("#product select").val().indexOf(";n") > 0 ){
			$( "#product .ships" ).html( defaultShippingStatus );
			$( "#product .ships" ).addClass("hidden");
			if( defaultShippingOutOfStock == true ){
				$( "#product .ships" ).addClass("outofstock");
			}else{
				$( "#product .ships" ).removeClass("outofstock");
			}
			return;
		}else{
			$( "#product .ships" ).removeClass("hidden")
		}
		
		for(var i = 0; i < window.options.length; i++){
			if( window.options[i].value == $("#product select").val() ){
				if(window.options[i].status.hint){
					$( "#product .ships" ).html( "<span>" + window.options[i].status.message + '<span class="q"><span>' + window.options[i].status.hint + "</span></span></span>");	
				}else{
					$( "#product .ships" ).html( "<span>" + window.options[i].status.message + "</span>");	
				}
				
				if( window.options[i].status.color && window.options[i].status.color == "red"){
					$( "#product .ships" ).addClass("outofstock");
				}else{
					$( "#product .ships" ).removeClass("outofstock");
				}
				
				if( window.options[i].status.isAvailable == true){
					$("#product fieldset.qty input[type='text'], #product fieldset.qty input[type='submit']").show();
				}else{//
					$("#product fieldset.qty input[type='text'], #product fieldset.qty input[type='submit']").hide();
				}
				break;
			}
		}		
	}
	
	if(window.ss_getinfo){
		ss_getinfo_old = ss_getinfo;
		ss_getinfo = function(ss, recid, level){
			updateShippingStatus()
			ss_getinfo_old(ss, recid, level);
			
			if($("#product select").size() == level){
//need to update price if necessary
	if(priceHTML == null){
		$("#product div.price").find("script").remove();
		priceHTML = $("#product div.price").html();
	}
	if(ss.options[ss.selectedIndex].value.indexOf(";n") > 0){
		$("#product div.price").html( priceHTML );
	}else{
		var _priceHTML = ss.options[ss.selectedIndex].value;
		if(_priceHTML.indexOf(";") >= 0){
			_priceHTML = _priceHTML.substring(_priceHTML.indexOf(";") + 1)
			if(_priceHTML.indexOf("=") >= 0){
				_priceHTML = _priceHTML.substring(_priceHTML.indexOf("=") + 1)
			}
			$("#product div.price").html("$" + numberWithCommas( (basePrice + parseFloat(_priceHTML)).toFixed(2) ));
		}else{
			$("#product div.price").html( "$" + numberWithCommas (basePrice.toFixed(2)) );
		}
	}

			}
			
		}
	}else{
	
		$("#product select").bind("change", function(){
			updateShippingStatus()
		})
		$("#product select").trigger("change")
		
	}
}

var priceHTML = null;
$("#product select").bind("change", function(){
	if(priceHTML == null){
		$("#product div.price").find("script").remove();
		priceHTML = $("#product div.price").html();
	}
	if(this.options[this.selectedIndex].value.indexOf(";n") > 0){
		$("#product div.price").html( priceHTML );
	}else{
		var _priceHTML = this.options[this.selectedIndex].value;
		if(_priceHTML.indexOf(";") >= 0){
			_priceHTML = _priceHTML.substring(_priceHTML.indexOf(";") + 1)
			if(_priceHTML.indexOf("=") >= 0){
				_priceHTML = _priceHTML.substring(_priceHTML.indexOf("=") + 1)
			}
			$("#product div.price").html("$" + numberWithCommas( (basePrice + parseFloat(_priceHTML)).toFixed(2) ));
		}else{
			$("#product div.price").html( "$" + numberWithCommas (basePrice.toFixed(2)) );
		}
	}
})


	
	$("table.cart td.cart_op").each(function(){
		var newHTML = "";
		if( $(this).find("table.giftcert").size() >0 ){
			newHTML = '<table class="giftcert">' + $(this).find("table.giftcert").html().replace(/::/g, ":") + "</table>";
		}else{
			$(this).find("table td").each(function(){
				var _option = $(this).text();
				if( _option.indexOf("&") !== -1 ){
					var _index = $("table.cart td.cart_name").index( $(this).closest("table").closest("tr").prev().find("td.cart_name").eq(0) ) 
					if( _index !== -1 ){
						_option = ss_finite_options[ _index ];
					}
				}
				newHTML += '<div class="cart_op">' + _option + '</div>';
			})
		}
		
		$(this).closest("tr").prev().find("td.cart_name").append( newHTML );
		$(this).closest("tr").remove();
	})	
	
	ss_QOH = new Array();
	$('table.cart td.cart_sku').each(function() {
		var currentindex = $(this).closest("tr").index() - 1;
		var productSKU = $(this).text();
		if(productSKU.length == 0){//gift sertifiacate for example
			return;
		}
		var ajaxurl = "";
		
		if( $(this).closest("tr").find(".cart_op").size() == 0 ){
			ajaxurl = '/scripts/getQohAndField13BySku.php?sku=' + productSKU	
		}else{
			ajaxurl = '/scripts/getQohAndField13BySku.php?sku=' + productSKU + "&option=" + encodeURIComponent( $.trim( $(this).closest("tr").find(".cart_op").text()) );
		}
		
		var $thisobject = $(this);
		
		$.getJSON(ajaxurl, function(data) {
			var n = parseInt( data.QOH );
			ss_QOH[currentindex] = n;			
			var f13 = data.Field13;
			ss_field13[currentindex] = escape(f13);
			
			if( isNaN(n) ){
				n = 0
			};
			
			if(n < 0){
				n = 0
			};
			var parts = f13.split(':');
			var p = parts[0];
			
			var inv = new Array();
			inv['A'] = Array('1', 'Back Ordered');
			inv['B'] = Array('1', 'Pre-Order - Ships Upon Release');
			inv['C'] = Array('1', 'Out of Stock');
			inv['D'] = Array('DISCONTINUED! Get one of the last ' + n + ' available.', 'Discontinued!');
			inv['E'] = Array('1', 'Usually ships in 1-2 business days');
			inv['F'] = Array('1', 'Usually ships in 1-3 business days');
			inv['G'] = Array('1', 'Usually ships in 2-5 business days');
			inv['H'] = Array('1', 'Usually ships in 4-7 business days');
			inv['I'] = Array('1', 'Usually ships in 4-8 business days');
			inv['J'] = Array('1', 'Usually ships in 7-10 business days');
			inv['K'] = Array('1', 'Usually ships in 1-2 weeks');
			inv['L'] = Array('1', 'Usually ships in 4-6 weeks');
			inv['Q'] = Array('1', 'Usually ships in 2-4 weeks');
			inv['M'] = Array('1', 'Usually ships in 2-4 business days');
			inv['N'] = Array('1', 'Usually ships in 10-14 business days');
			inv['O'] = Array('1', 'Not available for online checkout');
			inv['P'] = Array('1', 'Awaiting Repress - Ships Upon Availability');
			inv['R'] = Array('1', 'Awaiting Stock – Ships Upon Availability');
			
			var status = "";
			switch (p){
				case "E":
				case "F":
				case "G":
				case "H":
				case "I":
				case "J":
				case "K":
				case "L":
				case "M":
				case "N":
				case "Q":
					if(n == 0) {
						status = inv[p][1];
					} else if(n <= 3) {
						status = "Hurry, only " + n + " left! Usually ships within one business day!";
					} else {
						status = "In stock, usually ships within one business day.";
					}
					break;
				case "B":
					if( n <= 0){
						status 	= "Pre-Order - Ships Upon Release";
					}else if(n <= 3){
						status = "Hurry, only " + n + " left! Usually ships within one business day!";
					}else{//$quantityOnHand > 3
						status = "In stock, usually ships within one business day";
					}
					break;
				case "P":
					if( n <= 0){
						status 	= "Awaiting Repress - Ships Upon Availability";
					}else if(n <= 3){
						status = "Hurry, only " + n + " left! Usually ships within one business day!";
					}else{//$quantityOnHand > 3
						status = "In stock, usually ships within one business day";
					}
					break;
				case "O":
					status = inv[p][1];
					break;
				case "C":
					if(n > 3) {
						status = "In stock, usually ships within one business day.";
					} else if(n <= 3 && n != 0) {
						status = "Hurry, only " + n + " left! Usually ships within one business day!";
					} else {
						status = "Out Of Stock";
					}
					break;
				case "D":
					if(n > 0) {
						status = "Discontinued, Get one of the last " + n + " available!";
					} else {
						status = "Discontinued";
					}
					break;
				case "R":
					if(n > 3) {
						status = "In stock, usually ships within one business day.";
					} else if(n <= 3 && n != 0) {
						status = "Hurry, only " + n + " left! Usually ships within one business day!";
					} else {
						status = "Awaiting Stock - Ships Upon Availability";
					}
					break;
			}		
			if(status.indexOf("In Stock") >= 0 || status.indexOf("In stock") >= 0 || status.indexOf("Hurry, only") >= 0){
				var newhtmlvalue = '<div class="instock">' + status + '</div>';
			}else{
				var newhtmlvalue = '<div class="outofstock">' + status + '</div>';
			}			
			$thisobject.closest("tr").find('td.cart_name').append(newhtmlvalue);
			
		});
	});

	$("td.ship_addr_hdr, td.bill_addr_hdr").each(function(){
		if( $(this).html().indexOf("Shipping Address") >= 0 ){
			$(this).html("<h3>Shipping Address</h3>");
		}else{
			$(this).html("<h3>Billing Address</h3>");
		}
	})
	
	//$("td.ship_addr_hdr").html("<h3>Shipping Address</h3>");
	//$("td.bill_addr_hdr").html("<h3>Billing Address</h3>");	
	if( $("form.cr").size() == 0 && $("table.addr .amazon_address").size() == 0){
		var newHtml = $("table.addr > tbody > tr > td").eq(0).html() + $("table.addr > tbody > tr > td").eq(1).html();
		if( $("table.addr > tbody > tr > td").size() > 2 ){
			newHtml += '<p class="addr_foot">' + $("table.addr > tbody > tr > td").eq(2).html() + "</p>";
		}
		$("table.addr").replaceWith( newHtml );
	}else{
		$("table.addr").show();
	}
	
	$("#paypal_button input").attr("width", null).attr("height", null).attr("src", "/media/images/sc/pp.png");
	
	
	if( $(window).width() < 960 ){
		$("th.cart_quantity").text("qty");
		
		$("body.cart table.cart td.cart_quantity").each(function(){
			$(this).append( $(this).closest("tr").find("td.cart_delete").html() )
			$(this).closest("tr").find("td.cart_delete").remove();
		})
		$("body.cart table.cart td.cart_op1, table.cart th.cart_delete").remove();
	}	
	
	$("input[name='coupon_code']").attr("placeholder", "Coupon Code")
	
	$('div.giftcert').contents().filter(function(){
    	return this.nodeType === 3;
	}).remove();
	
	$("input[name='giftcert_code']").attr("placeholder", "Certificate Number")
	$("input[name='giftcert_pin']").attr("placeholder", "PIN")

	$('body.checkout table.payment td.payment_value').contents().filter(function(){
		return (this.nodeType === 3 && $.trim(this.innerHTML)=="");
	}).remove();
	
	
	if($("table.ship_addr input").size() > 0){
		if( authorized() == true){
			$(".ship_check").remove();
			$(".ship_addr input, .ship_addr select").attr("disabled", null);
			
			
			$("table.bill_addr, table.ship_addr").addClass("authorized");
			$("table.bill_addr > tbody > tr:first-child").after('<tr><td colspan="2" class="copyshiptobill"><input type="checkbox" id="useshipping" name="useshipping"><span>Check here if billing and shipping address are the same</span></td></tr>');			
		}else{
			if( $(".ship_check").size() == 0 ){			
				$("table.ship_addr > tbody > tr:first-child").after('<tr><td colspan="2" class="copybilltoship"><input type="checkbox" id="usebilling" name="usebilling"><span>Check here if shipping and billing are the same</span></td></tr>');
			}else{				
				$(".ship_check input[type='checkbox']").attr("id", "usebilling");
				if( $(".ship_check input[type='checkbox']:checked").size() > 0 ){
					syncBillingAndShipping();
					
					$("table.ship_addr input[type='text']").keyup(uncheckUseBilling)
					$("table.ship_addr select").click(uncheckUseBilling)

					$("table.bill_addr input[type='text']").keyup(syncBillingAndShipping);
					$("table.bill_addr select").change(syncBillingAndShipping);
				}
			}
		}
	}
	
	$("#usebilling").click(function(){
		if (this.checked){
    		syncBillingAndShipping()
    
    		$("table.ship_addr input[type='text']").keyup(uncheckUseBilling)
    		$("table.ship_addr select").click(uncheckUseBilling)

    		$("table.bill_addr input[type='text']").keyup(syncBillingAndShipping);
    		$("table.bill_addr select").change(syncBillingAndShipping);
  		}
	})
	$("#useshipping").click(function(){
		if (this.checked){
    		syncShippingAndBilling()
    
    		$("table.bill_addr input[type='text']").keyup(uncheckUseShipping)
    		$("table.bill_addr select").click(uncheckUseShipping)

    		$("table.ship_addr input[type='text']").keyup(syncShippingAndBilling);
    		$("table.ship_addr select").change(syncShippingAndBilling);
  		} 
	})
	
	function uncheckUseBilling(e){
		var name = $(this).attr("name").substring(4);
		if( $(this).val() != $("table.bill_addr *[name='" + name + "']").val() ){
			$("#usebilling").prop("checked", false)
		}
	}
	function uncheckUseShipping(e){
		var name = $(this).attr("name"); //need to remove Ship from the begging, ex ShipLast
		if( $(this).value != $("table.ship_addr *[name='Ship" + name + "']").attr("name")){
			$("#useshipping").prop("checked", false)
		}
	}
	function syncBillingAndShipping(){
		if ($("#usebilling:checked").size() > 0){
			var names = ["Title", "First", "Middle", "Last", "Suffix", "Company", "Address", "Address2", "City", "State", "Zip", "Country", "Phone"]
			
			for(i = 0; i < names.length; i++){
				var name = names[i];
    			if ( (document.billing.elements['Ship' + name] != undefined) && (document.billing.elements[name] != undefined) ){          	
    				document.billing.elements['Ship' + name].value = document.billing.elements[name].value;
    			}
			}
		}
	}
	function syncShippingAndBilling(){
		if ($("#useshipping:checked").size() > 0){
			var names = ["Title", "First", "Middle", "Last", "Suffix", "Company", "Address", "Address2", "City", "State", "Zip", "Country", "Phone"]
			
			for(i = 0; i < names.length; i++){
				var name = names[i];
    			if ( (document.billing.elements['Ship' + name] != undefined) && (document.billing.elements[name] != undefined) ){          	
    				document.billing.elements[name].value = document.billing.elements['Ship' + name].value;
    			}
			}
		}
	}	
	
	
	$("input[name='ShipZip']").parents("td").append('<div id="zipnotice">IF you change your shipping address ZIP CODE you will need to go back to the previous page of the shopping cart so your shipping rates can be recalculated.</div>')
	
	$("input[name='ShipZip']")
		.focus(function(){
			$("#zipnotice").fadeIn();
		})
		.blur(function(){
			$("#zipnotice").fadeOut();
		})
	
	$("table.zipncountry td.zipncountry").first().append('<input type="image" border="0" align="bottom" onclick="return(CheckIt(7,0));" title="Update" alt="Update" name="Update" id="Recalculate" class="button383" src="/media/images/sc/update.png">')
	
	$("table#ship_options").after('<input type="button" onclick="ss_jQuery(\'#Recalculate\').click()" value="Update Shipping" />')
	
	
	/* Customer registration pages */
	function extractEmails (text){
		return text.match(/([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/gi);
	}
	
	if( $("h1 .trackmyorder a").size() > 0 ){

		$("table.addr td.addr_val").each(function(){
			var results = extractEmails( $(this).text() );
			if(results != null){
				$("h1 .trackmyorder a").attr("href", $("h1 .trackmyorder a").attr("href") + results[0]);
			}
		})
		$("h1 .trackmyorder").show();
	}
	
	
	if($("#forgotpasswordpopup").size() > 0){
		$("#forgotpasswordpopup").popup({transition: 'all 0.3s'});
	
		$(".crlogin form").validate();	
		$("#forgotpasswordpopup form input[name=cr_type]").val("23");
		
		$("#forgotpasswordpopup form").validate({
		 	submitHandler: function(form) {
		 	
    		$("#forgotpasswordpopuploading").show()
    		
    		
    		$.ajax({
  				type: $(form).attr("method"),
  				url: $(form).attr("action"),
  				data: $(form).serialize(),
  				success: function(data){
  					$("#forgotpasswordpopuploading").addClass("loading-no").empty().append( $(data).find("form.cr p").first().text() );
  				},
  				error: function(data){
  					$("#forgotpasswordpopuploading").addClass("loading-no").empty().append( "Something wrong. Please try again later." );
  				}
			});
			
    		return false;			 	
  		}
		
	});
			
	}
	
	if($(".regfrm form").size() > 0){
		$(".regfrm form").validate();
	}
	
	
	$("#messages").each(function() {
    	if ($.trim($(this).html())){
        	$(this).show();
    	}
	});
/* End Customer registration pages */	
	
	
	
	
	
	
});

$(document).ready(function(){
	if( $("a.menu-link:visible").size() > 0 ){
		$("body > header form input[type='text'], #search form input[type='text']").attr("placeholder", "Search Our Store");
	}
	
/* Reviews functions */	
$("div.reviews_form .review_email_field em").remove();
$("div.reviews_form .review_email_field input[name='email']").removeClass("required").attr("name", "email_").after($('<input type="hidden" name="email" />'))
$("div.reviews_form .reviews_submit").click(function(){
	if($(this).parents("div.reviews_form").find("input[name='email_']").val() == ""){
		$(this).parents("div.reviews_form").find("input[name='email']").val("email@placeholder.com")
	}else{
		$(this).parents("div.reviews_form").find("input[name='email']").val($(this).parents("div.reviews_form").find("input[name='email_']").val())
	}
})

$("div.reviews_form div.reviews_stars em").remove();
$("div.reviews_form div.reviews_stars_rating").css("width", "100%")
$("div.reviews_form input[name='current_rating']").val(100);
$("div.reviews_form input[name='rating']").val(100);


$("div.reviews_form").each(function(index, div){
	if(index % 2 == 0){
		$(div).addClass("cl");
		return;
	}
	
	var height = Math.max($(div).find("h2").height(), $(div).prevAll("div.reviews_form").find("h2").height());
	
	$(div).find("h2").css("minHeight",  height + "px");	
	$(div).prevAll("div.reviews_form").find("h2").css("minHeight", height + "px");
	
	var height = Math.max($(div).find("div.reviews_suggestions").height(), $(div).prevAll("div.reviews_form").find("div.reviews_suggestions").height());
	
	$(div).find("div.reviews_suggestions").css("minHeight",  height + "px");	
	$(div).prevAll("div.reviews_form").find("div.reviews_suggestions").css("minHeight", height + "px");	

	height = Math.max($(div).height(), $(div).prevAll("div.reviews_form").height()) - 24;
	$(div).css("minHeight", height + "px");
	$(div).prevAll("div.reviews_form").css("minHeight", height + "px")
	
})

	
	var max_stars = 5;
	var max_length = 1000;
	var state = {
    	rating: 0
  	}
	
	$('textarea[name="reviews_area"]').bind('paste keydown', function() { 
    	var text = $(this).val(); 
    	var len = text.length;
    	if (len > max_length) {
      		$(this).val(text.substr(0, max_length));
      		len = max_length;
    	}
    	$(this).nextAll('.character_count').find('span').html(max_length - len);
  	});

  	if($('textarea[name="reviews_area"]').length > 0){
	   	var text = $('textarea[name="reviews_area"]').val(); 
   		var len = text.length;
   		if (len > max_length) {
			$('textarea[name="reviews_area"]').val(text.substr(0, max_length));
      		len = max_length;
    	}
  	}
    
    
    $('textarea[name="reviews_area"]').nextAll('.character_count').find('span').html(max_length - len);
          	
	$('.new_review_stars_wrapper a').hover(function() {        
		var star_num = parseInt($(this).html());
		$('.new_review_stars_rating').css({
			'width': ((star_num + 1)* 100) / max_stars + "%"
		});
	},
	function(){		
		state.rating = parseInt($('#newform input[name="current_rating"]').val());
		if(!state.rating){
			state.rating = 0;
		}
		$('.new_review_stars_rating').css({
          'width': state.rating + "%"
        });
      });
    
    
    $('.new_review_stars_wrapper a').click(function() {
      var rating = (parseInt($(this).html()) + 1) / max_stars * 100;
      $('#newform input[name="current_rating"]').val(rating);
      $('#newform input[name="rating"]').val(rating);
      state.rating = rating;
      $("#current_rating").valid();
    }); 
    
    $("#newform #recaptcha_response_field").addClass("required")
    var newreview = $("#newform form").validate();
    
    
    $("#newform .cancel").click(function(){    	
    	$.fancybox.close();

    	$("#newform	form")[0].reset();
		state.rating = parseInt($('#newform input[name="current_rating"]').val());
		$('.new_review_stars_rating').css({
          'width': state.rating + "%"
        });
        $("#current_rating").valid();
    })
    
    $("#newform form").submit(function(e){
    	
		$('#newform .save').val("Working...");
		$('#newform .save').attr("disabled", "disabled");
		$('.captcha_error').css('display', 'none');
      	$.ajax({
    		url: $(this).attr("action"),
    		type: "POST",
    		data: $(this).serialize(),
    		success: function(response){
    			
				$('#newform .save').val("Submit Review");
				$('#newform .save').removeAttr("disabled");
				
				if (response.search("CAPTCHA error") == -1) {
					$.fancybox("<h2>Thank you for your review!</h2> <input type=\"button\" value=\"Close\" onclick=\"$.fancybox.close();\" />");
					$.fancybox.resize();
					$.fancybox.center();
				} else {
					$('.captcha_error').css('display', 'block');
					Recaptcha.reload();
          		}
          		
    		}
    		
    	})
    	e.preventDefault()
    })


$("#newreview").click(function(e){	
	$.fancybox(
		{
			href: "#newform",
			type: "inline",
			
        	'autoDimensions'	: false,
			'width'         	: "600px",
			'height'        	: "700px"
		}
	);
	e.preventDefault();
	return false;
})
/* End Reviews functions */
})
