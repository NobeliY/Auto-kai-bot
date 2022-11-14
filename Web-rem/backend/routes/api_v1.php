<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;


Route::middleware('auth:sanctum')->get('/admin', function (Request $request) {
    return $request->user();
});

Route::post('/login', [\App\Http\Controllers\api\v1\AdminController::class, "login"]);
Route::get('/logout', [\App\Http\Controllers\api\v1\AdminController::class, "logout"]);
