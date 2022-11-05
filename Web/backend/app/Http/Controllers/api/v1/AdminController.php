<?php

namespace App\Http\Controllers\api\v1;

use App\Http\Controllers\Controller;
use App\Models\Admin;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Auth;

class AdminController extends Controller
{
    public function login(Request $request): JsonResponse
    {
        $credentials = $request->only('login', 'password');

        if (Auth::attempt($credentials))
        {
            $authUser = auth()->user();
            return response()->json([
                'message' => 'Login Success',
            ], 200);
        }
        else
            return response()->json([
                'message' => 'Invalid login or password',
            ], 401);
    }

    public function logout(): JsonResponse
    {
        Auth::logout();
        return \response()->json([
            'message' => 'Logged out',
        ], 200);
    }
}
