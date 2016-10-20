var code ; //在全局 定义验证码

function createCode(){ 
	code = new Array();
	var codeLength = 2;//数字个数
	var checkCode = $("#checkCode");
	checkCode.val("");

//	var selectChar = new Array(2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z');
    var selectChar = new Array(0,1,2,3,4,5,6,7,8,9,10);

    var codeArr = [];
	for(var i=0;i<codeLength;i++) {
	   var charIndex = Math.floor(Math.random()*11);
	   codeArr.push(selectChar[charIndex]);
	}
    var selectFlag = new Array('+', '-', '*', '/');
    var flagIndex = Math.floor(Math.random()*4);
    var flag = selectFlag[flagIndex];

	if(codeArr.length != codeLength){
	   createCode();
	}

	var exp = '' + codeArr[0] + flag + codeArr[1];
    code = eval(exp);
	checkCode.val(exp);
}
createCode();

function validate() {
	var inputCode = $("#id_code").val();
	if(inputCode.length <=0) {
	   $('#err_code').text("请输入验证码！");
	   return false;
	}else if(inputCode != code ){
	   $('#err_code').text("验证码输入错误！");
	   createCode();
	   return false;
	}else {
	   return true;
	}
}
